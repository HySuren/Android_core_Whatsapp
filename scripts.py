import sys
from usefull_scripts import anti_overheat, check_ip, reinstall_whatsapp, reboot, props, payment, backup, randomize_contacts, volume, check_contacts, delete_meta_apps, delete_proxy, delete_sms, disable_adb_timeout


match sys.argv:
    case _, '--wa':
        reinstall_whatsapp.run()

    case _, '--ip':
        check_ip.run()

    case _, '--heat':
        anti_overheat.run()

    case _, '--proxy':
        delete_proxy.run()

    case _, '--reboot':
        reboot.run()

    case _, '--prop':
        props.change_props()

    case _, '--rprop':
        props.rollback_props()

    case _, '--eprop':
        props.enable_props()

    case _, '--gprop':
        props.get_props()

    case _, '--iprop':
        props.install()

    case _, '--pay':
        payment.pay_all_safe()

    case _, '--pay_mobile':
        payment.pay_mobile()

    case _, '--pay', '--hard':
        payment.pay_all()

    case _, '--pay', '--safe':
        payment.pay_all_safe()

    case _, '--pay', phone_or_serial:
        if phone_or_serial.isdigit():
            payment.pay_by_phone(phone_or_serial)
        else:
            payment.pay_by_serial(phone_or_serial)

    case _, '--pay', phone, price:
        payment.pay_by_phone(phone, price)

    case _, '--cont':
        randomize_contacts.run()

    case _, '--chcont':
        check_contacts.run()

    case _, '--volume':
        volume.run()

    case _, '--removemeta':
        delete_meta_apps.run()

    case _, '--backup', '-l':
        backup.backup_locally()

    case _, '--sms':
        delete_sms.run()

    case _, '--disable':
        disable_adb_timeout.run()

    case *_, :
        print('''Parameters:
    --wa : install whatsapp
    --ip : get ip of all devices
    --heat : close overheat window on all devices
    --reboot : reboot all devices
    --prop : change props for all devices
    --rprop : rollback props for all devices
    --eprop : enable props in Magisk for all devices (necessary to enable all props before change them)
    --gprop : show prop-fingerprint and prop id in db if it change, else insted of id write None
    --iprop : install props package
    --pay [phone | serail] [price]:
        if no args - check all unpayed devices in db and pay for them default price
        if second arg exist (must be phone or serial), pay for concrete phone with dfault price price. 
        feared arg is optional, if u pay for conret phone u can show
    --cont: randomize contacts on all devices
    --chcont: check contacts on all devices
    --volume: turn volume on
        
''')
