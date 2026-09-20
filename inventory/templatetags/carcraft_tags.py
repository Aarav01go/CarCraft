from decimal import Decimal
from django import template

register = template.Library()


def format_indian_number(value, include_decimals=False):
    """
    Format a number in Indian numbering system:
    e.g. 1000 -> 1,000
         100000 -> 1,00,000 (1 Lakh)
         2450000 -> 24,50,000 (24.5 Lakhs)
         10000000 -> 1,00,00,000 (1 Crore)
    """
    if value is None or value == '':
        return ''
    
    try:
        if isinstance(value, str):
            clean_str = value.replace('₹', '').replace('$', '').replace(',', '').strip()
            val_float = float(clean_str)
        elif isinstance(value, Decimal):
            val_float = float(value)
        else:
            val_float = float(value)
    except (ValueError, TypeError):
        return str(value)

    is_negative = val_float < 0
    val_float = abs(val_float)

    if include_decimals:
        parts = f"{val_float:.2f}".split('.')
        int_part = parts[0]
        dec_part = '.' + parts[1]
    else:
        # Check if original value had fractional cents/paise
        formatted_2dp = f"{val_float:.2f}"
        parts = formatted_2dp.split('.')
        if parts[1] == '00':
            int_part = str(int(val_float))
            dec_part = ''
        else:
            int_part = parts[0]
            dec_part = '.' + parts[1]

    # Indian grouping: last 3 digits, then every 2 digits
    if len(int_part) <= 3:
        formatted_int = int_part
    else:
        last_three = int_part[-3:]
        remaining = int_part[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted_int = ','.join(groups) + ',' + last_three

    sign = '-' if is_negative else ''
    return f"{sign}{formatted_int}{dec_part}"


@register.filter(name='inr')
def inr_filter(value, show_decimals=False):
    """Format value as Indian Rupee string: e.g. ₹24,50,000"""
    if value is None or value == '':
        return '₹0'
    formatted = format_indian_number(value, include_decimals=bool(show_decimals))
    return f"₹{formatted}"


@register.filter(name='indian_number')
def indian_number_filter(value):
    """Format a number with Indian comma grouping without currency symbol."""
    if value is None or value == '':
        return '0'
    return format_indian_number(value, include_decimals=False)

