# written by cragson
#!/usr/bin/env python

import csv
import os.path

wallet = { "EUR": 0.0, "USD": 0.0, "GBP": 0.0, "RUB": 0.0 }

filter_list = []

def parse_all_filter():
    global filter_list
    ret = []
    with open( "filter.list", 'r', encoding='utf-8') as _filter:
        _content = _filter.readlines()
        for _elem in _content:
            ret.append( _elem.strip() )
    _filter.close()

    filter_list = ret

    return

def parse_all_currencies( data ):
    currencies = []
    for _elem in data:
        if _elem["Währung"] not in currencies:
            currencies.append( _elem["Währung"] )
    return currencies

def check_if_csv_exists():
    _file = os.path.isfile("Download.CSV")

    if _file:
        print("[+] Found the paypal report csv file!")
    else:
        print("[!] Error while searching the paypal report csv file!")
        exit()

def parse_csv_as_list():
    ret = []
    with open( "Download.CSV", 'r', encoding='utf-8') as _csv_file:
        data = csv.DictReader( _csv_file )
        for _elem in data:
            ret.append( _elem )
    _csv_file.close()

    return ret
        

def parse_brutto_price_from_entry( ENTRY ):

    # Datum,"Uhrzeit","Zeitzone","Name","Typ","Status","Währung","Brutto","Gebühr","Netto","Absender E-Mail-Adresse","Empfänger E-Mail-Adresse","Transaktionscode","Lieferadresse","Adress-Status","Artikelbezeichnung","Artikelnummer","Versand- und
    pass

def main():
    
    global wallet, filter_list

    parse_all_filter()

    print( filter_list )

    
    print("[+] PayPal Tears [+]")
    print("\t Heul nicht, wenn du siehst wie viel Kohle du über PayPal verballert hast!")

    check_if_csv_exists()
    
    data = parse_csv_as_list()

    _found_currencies = parse_all_currencies( data )

    print("[+] Found", len( _found_currencies ), "different currencies:", " ".join( _found_currencies ) )
    print("[!] Using static information for currency exchange values.")

    kohle = 0.0

    is_filter_enabled = len( filter_list ) > 0

    print( len( filter_list ) )

    elem_found = False
    
    for _elem in data:

        if "Zahlung" not in _elem["Typ"]:
            continue

        if is_filter_enabled:
            for current_filter in filter_list:
                if current_filter in _elem["Name"].strip().lower():
                    elem_found = True

        if( is_filter_enabled and elem_found == False ):
            continue

        elem_found = False
        
        val = float( _elem["Brutto"].replace("-", "" ).replace(".", "" ).replace("," ,"." ) )

        # DD.MM.YY
        # 27.09.20
        # https://www.x-rates.com/table/?from=EUR&amount=1
        currency = _elem["Währung"]

        if currency in wallet:
            wallet[currency] += val
            print("[Info][", _elem["Name"].strip(),"] Adding", val, "to", currency)
        else:
            print( "[!] Found a not implemented currency:", currency )
            exit()
        
        if( currency == "EUR" ):
            val *= 1.0

        elif( currency == "USD" ):
            val *= 0.85

        elif( currency == "GBP" ):
            val *= 1.1

        elif( currency == "RUB" ):
            val *= 0.011
        
        kohle += val
        val = 0

    for _key in sorted( wallet.keys() ):
        print(_key, "=>", round( wallet[ _key ], 2 ) )

    if is_filter_enabled:
        print( "[+] Used filters:", " ".join( filter_list ) )
    else:
        print( "[-] No filter were used!" )
        
    print( "\n[>] Kohle verballert:", round( kohle, 2 ), "€" )
    


if __name__ == '__main__':
    main()
