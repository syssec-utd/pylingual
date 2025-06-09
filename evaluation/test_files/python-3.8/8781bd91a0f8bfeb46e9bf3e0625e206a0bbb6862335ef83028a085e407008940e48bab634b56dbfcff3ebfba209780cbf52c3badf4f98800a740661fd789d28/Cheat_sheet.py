from cyberonix.main.tools import banner, run_on_browser, colors, template
import os
import threading, inspect

def main():
    if inspect.stack()[1].function != 'main':
        if not main.called:
            main.called = True
            start()
    else:
        start()

def start():
    os.system('clear')
    banner.main()
    banner.attack('Cheat Sheet')
    cheat({'Nmap cheatsheet': 'https://www.tutorialspoint.com/nmap-cheat-sheet', 'Maltego cheatsheet': 'https://static.maltego.com/cdn/case%20studies/building-integrations-for-maltego-cheat-sheet.pdf', 'Hping3 cheatsheet': 'https://cyberwar.nl/d/cheatsheets/hping3_cheatsheet_v1.0-ENG.pdf', 'Netdiscover cheatsheet': 'https://linuxcommandlibrary.com/man/netdiscover', 'Wafw00f cheatsheet': 'https://cheatsheet.haax.fr/web-pentest/applicative-scans/web_application_firewall/', 'Metasploit-Framework cheatsheet': 'https://cdn.comparitech.com/wp-content/uploads/2019/06/Metasploit-Cheat-Sheet-1.webp', 'Wireshark cheatsheet': 'https://www.stationx.net/wireshark-cheat-sheet/', 'Bettercap cheatsheet': 'https://www.bettercap.org/usage/interactive/', 'Tcpdump cheatsheet': 'https://cdn.comparitech.com/wp-content/uploads/2019/06/tcpdump-cheat-sheet-1.pdf', 'Scapy cheatsheet': 'https://wiki.sans.blue/Tools/pdfs/ScapyCheatSheet_v0.2.pdf', 'Responder cheatsheet': 'https://www.ivoidwarranties.tech/posts/pentesting-tuts/responder/cheatsheet/', 'Airgeddon cheatsheet': 'https://liodeus.github.io/2020/10/29/OSWP-personal-cheatsheet.html#airgeddon', 'Wpscan cheatsheet': 'https://linuxcommandlibrary.com/man/wpscan', 'Wapiti cheatsheet': 'https://wapiti.limsi.fr/manual.html', 'Legion cheatsheet': 'https://theory.stanford.edu/~aiken/LegionRetreat21/slides/Tools.pdf', 'Nikto cheatsheet': 'https://cdn.comparitech.com/wp-content/uploads/2019/07/NIkto-Cheat-Sheet.pdf', 'Burp Suite cheatsheet': 'https://portswigger.net/burp/documentation/desktop', 'Owasp ZAP cheatsheet': 'https://www.zaproxy.org/docs/desktop/cmdline/', 'Nessus cheatsheet': 'https://limberduck.github.io/nessus-cheat-sheet/nessus-cheat-sheet.pdf', 'dirb cheatsheet': 'https://manpages.debian.org/unstable/dirb/dirb.1.en.html', 'skipfish cheatsheet': 'https://linux.die.net/man/1/skipfish', 'Nuclei cheatsheet': 'https://cheatsheet.haax.fr/web-pentest/tools/nuclei/', 'Wifite cheatsheet': 'https://cheatography.com/socket23/cheat-sheets/wifite/', 'Aircrack-ng cheatsheet': 'https://www.cyberfella.co.uk/rhel/aircrack-ng-suite.pdf'}, 'cheatSheet')

def exit_program():
    os.system('clear')
    banner.main()
    print('\x1b[38;5;105m', '[+] Thanks visit again'.title())

def cheat(cheatSheet, name):
    while True:
        os.system('clear')
        banner.main()
        banner.attack(name.title())
        key = list(cheatSheet.keys())
        key.append('go back'.title())
        for i in range(len(key)):
            print(colors.options, f'{i}) {key[i]}'.title(), colors.reset)
        try:
            option = input(f'\n {colors.select}Select An Option ->{colors.reset}  ')
        except KeyboardInterrupt:
            template.exit_program()
        try:
            threading.Thread(target=run_on_browser.main, args=(cheatSheet[key[int(option)]],)).start()
        except:
            exit_program()
            return
main.called = False
if __name__ == '__main__':
    main()