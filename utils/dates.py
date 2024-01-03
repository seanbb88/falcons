def days_in_month(month):
    days_in_month = {
        1: 31, 
        2: 28, 
        3: 31,  
        4: 30, 
        5: 31,  
        6: 30, 
        7: 31,
        8: 31,
        9: 30,  
        10: 31, 
        11: 30,  
        12: 31, 
    }
    return days_in_month[month]

def idx_to_month_str(idx):
    month_str = { 
        1: '05',  
        2: '06', 
        3: '07',
        4: '08',
        5: '09',  
    }
    return month_str[idx]
