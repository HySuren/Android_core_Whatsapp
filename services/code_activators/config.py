from .base_activator import RegionsList, Region, ActivatorID


class ActivatorTimeout(object):
    GET_NUMBER_SECONDS = 0


class ActivatorName(object):
    SMS_ACTIVATE_LIKE = "sms_activate_like"
    SMS_ACTIVATE_RENT = "sms_activate_rent"
    SMS_ACTIVATE = "sms_activate"
    SMS_ACTIVATE2 = "sms_activate2"
    SMS_BEELINE = "sms_beeline"
    SMS_HUB = "sms_hub"
    FIVE_SIM = "five_sim"
    ONLINE_SIM = "online_sim"
    VAK_SMS = "vak_sms"
    DROP_SMS = "drop_sms"
    GSM = 'gsm'
    DROP_SMS_GETSMS = 'drop_sms_getsms'
    SMS_MAN = 'sms_man'

    ALL_NAMES = [SMS_ACTIVATE_LIKE, SMS_ACTIVATE_RENT, SMS_ACTIVATE, FIVE_SIM, ONLINE_SIM, VAK_SMS, DROP_SMS, GSM, DROP_SMS_GETSMS, SMS_BEELINE, SMS_HUB, SMS_MAN]


class KeyActivator:
    SMS_ACTIVATE = 'cb9bA84efAf7cAf0eA1ceb97f7309765'
    SMS_ACTIVATE2 = '64d77ffBcfec678398B1467547eB5e32'
    SMS_HUB = '161297U68e04019ec2349ece0aa2a2a549b1237'
    FIVE_SIM = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA0NjM3OTksImlhdCI6MTY1ODkyNzc5OSwicmF5IjoiYWJkNTc3MTk5NzM1NzRiNjNjNDM4ODZkYzRlYTgxY2QiLCJzdWIiOjY3NjczMn0.TD18R6Xa8PeLF0Ch4Xmi8dkIAmTi-t06oq_GlT4DUgi3GlDcHhH5nSSCwRx9ii5cj9_WVUISA3prSo6s7bpsFQcPi-nwO-VJTXL2C2fYMf6SKbVa4HjiGPTHKkjAcnr3NSbrqdYhDrdcYqi01x3_BBfsEOr1WuUqmBHHPnlBOLUgRvGLFPm5BMNZD69j_GfkpcRBtKYjEPUl0YVkJf5y_isypKoXb9hMdfTpmTFPorsLvt8tN9xd--emwPDccGmpQgkmLO-YL2i_mhZfkvu6jBRIr8-GEtpI39YsNO1vcZPRctPogO6YbzI1CENw9ZKFs_W2Zk1x_MHTripI8_Rkgw'
    ONLINE_SIM = 'fd4aa82d4c2b547b20dcd47c88b52631'
    # VAK_SMS = 'f3972c5533fb4816979ee360ec6a0dfd'
    # Для спама жесткого:
    VAK_SMS = 'c1f0b72d8aba420e8eef9d7759f735ac'
    # DROP_SMS = '614eedaf-a41a-4249-94f2-b51a6dcef349'
    # Для спама мягкого:
    DROP_SMS = 'efd36ed9-7a43-475c-8280-7b462993ccf7'
    SMS_MAN = 'QMfTES_N19AcxGPcJH1BLgJok6Goe6nm'

class PhonerStatus(object):
    class SmsActivateRu(object):
        """
        NUMBER_IS_READY                 - сообщить о готовности номера (смс на номер отправлено)
        ASK_FOR_ANOTHER_CODE            - запросить еще один код (бесплатно)
        COMPLETE_ACTIVATION             - завершить активацию
        CANCEL_ACTIVATION               - сообщить о том, что номер использован и отменить активацию
        """
        NUMBER_IS_READY = 1
        ASK_FOR_ANOTHER_CODE = 3
        COMPLETE_ACTIVATION = 6
        CANCEL_ACTIVATION = 8

        ALL_STATUSES = [NUMBER_IS_READY, ASK_FOR_ANOTHER_CODE, COMPLETE_ACTIVATION, CANCEL_ACTIVATION]

    class FiveSimNet(object):
        CANCEL = "cancel"
        FINISH = "finish"
        BAN = "ban"

        ALL_STATUSES = [CANCEL, FINISH, BAN]

    class OnlineSimRu(object):
        """
        OPERATION_OK                -
        OPERATION_REVISE            - Следует использовать, если поступил неверный код.
                                      Данный метод отправляет запрос на другой код в случае,
                                      если поступило несколько СМС на один номер с разными кодами.
        """
        OPERATION_OK = "operation_ok"
        OPERATION_REVISE = "operation_revise"

        ALL_STATUSES = [OPERATION_OK, OPERATION_REVISE]

    class VakSmsCom(object):
        """
        SEND        - отправлять запрос с параметрами status=send необходимо только в случае получения еще одной смс с кодом
        END         - отмена номера
        BAD         - номер уже использован, забанен
        """
        SEND = "send"
        END = "end"
        BAD = "bad"


class Countries:
    LATVIA = 'latvia'
    LITHUANIA = 'lithuania'
    ESTONIA = 'estonia'
    INDONESIA = 'indonesia'
    RUSSIA = 'russia'
    GERMANY = 'germany'
    KAZAKHSTAN = 'kazakhstan'
    FINLAND = 'finland'
    INDIA = 'india'
    CANADA = 'canada'
    USA = 'usa'
    VIETNAM = 'vietnam'
    IVORYCOAST = 'ivorycoast'
    NIGERIA = 'nigeria'
    GHANA = 'ghana'
    PAKISTAN = 'pakistan'
    AFGHANISTAN = 'afghanistan'
    ALBANIA = 'albania'
    ALGERIA = 'algeria'
    ANGOLA = 'angola'
    ANGUILLA = 'anguilla'
    ANTIGUAANDBARBUDA = 'antiguaandbarbuda'
    ARGENTINA = 'argentina'
    ARMENIA = 'armenia'
    ARUBA = 'aruba'
    AUSTRALIA = 'australia'
    AUSTRIA = 'austria'
    AZERBAIJAN = 'azerbaijan'
    BAHAMAS = 'bahamas'
    BAHRAIN = 'bahrain'
    BANGLADESH = 'bangladesh'
    BARBADOS = 'barbados'
    BELARUS = 'belarus'
    BELGIUM = 'belgium'
    BELIZE = 'belize'
    BENIN = 'benin'
    BHUTANE = 'bhutane'
    BIH = 'bih'
    BOLIVIA = 'bolivia'
    BOTSWANA = 'botswana'
    BRAZIL = 'brazil'
    BULGARIA = 'bulgaria'
    BURKINAFASO = 'burkinafaso'
    BURUNDI = 'burundi'
    CAMBODIA = 'cambodia'
    CAMEROON = 'cameroon'
    CAPEVERDE = 'capeverde'
    CAYMANISLANDS = 'caymanislands'
    CHAD = 'chad'
    CHILE = 'chile'
    CHINA = 'china'
    COLOMBIA = 'colombia'
    COMOROS = 'comoros'
    CONGO = 'congo'
    COSTARICA = 'costarica'
    CROATIA = 'croatia'
    CUBA = 'cuba'
    CYPRUS = 'cyprus'
    CZECH = 'czech'
    DJIBOUTI = 'djibouti'
    DOMINICA = 'dominica'
    DOMINICANA = 'dominicana'
    DRCONGO = 'drcongo'
    EASTTIMOR = 'easttimor'
    ECUADOR = 'ecuador'
    EGYPT = 'egypt'
    ENGLAND = 'england'
    EQUATORIALGUINEA = 'equatorialguinea'
    ERITREA = 'eritrea'
    ETHIOPIA = 'ethiopia'
    FRANCE = 'france'
    FRENCHGUIANA = 'frenchguiana'
    GABON = 'gabon'
    GAMBIA = 'gambia'
    GEORGIA = 'georgia'
    GREECE = 'greece'
    GRENADA = 'grenada'
    GUADELOUPE = 'guadeloupe'
    GUATEMALA = 'guatemala'
    GUINEA = 'guinea'
    GUINEABISSAU = 'guineabissau'
    GUYANA = 'guyana'
    HAITI = 'haiti'
    HONDURAS = 'honduras'
    HONGKONG = 'hongkong'
    HUNGARY = 'hungary'
    IRAN = 'iran'
    IRAQ = 'iraq'
    IRELAND = 'ireland'
    ISRAEL = 'israel'
    ITALY = 'italy'
    JAMAICA = 'jamaica'
    JAPAN = 'japan'
    JORDAN = 'jordan'
    KENYA = 'kenya'
    KUWAIT = 'kuwait'
    KYRGYZSTAN = 'kyrgyzstan'
    LAOS = 'laos'
    LESOTHO = 'lesotho'
    LIBERIA = 'liberia'
    LIBYA = 'libya'
    LUXEMBOURG = 'luxembourg'
    MACAU = 'macau'
    MADAGASCAR = 'madagascar'
    MALAWI = 'malawi'
    MALAYSIA = 'malaysia'
    MALDIVES = 'maldives'
    MALI = 'mali'
    MAURITANIA = 'mauritania'
    MAURITIUS = 'mauritius'
    MEXICO = 'mexico'
    MOLDOVA = 'moldova'
    MONGOLIA = 'mongolia'
    MONTENEGRO = 'montenegro'
    MONTSERRAT = 'montserrat'
    MOROCCO = 'morocco'
    MOZAMBIQUE = 'mozambique'
    MYANMAR = 'myanmar'
    NAMIBIA = 'namibia'
    NEPAL = 'nepal'
    NEWCALEDONIA = 'newcaledonia'
    NEWZEALAND = 'newzealand'
    NICARAGUA = 'nicaragua'
    NIGER = 'niger'
    NORTHMACEDONIA = 'northmacedonia'
    NORWAY = 'norway'
    OMAN = 'oman'
    PANAMA = 'panama'
    PAPUANEWGUINEA = 'papuanewguinea'
    PARAGUAY = 'paraguay'
    PERU = 'peru'
    PHILIPPINES = 'philippines'
    PUERTORICO = 'puertorico'
    QATAR = 'qatar'
    REUNION = 'reunion'
    ROMANIA = 'romania'
    RWANDA = 'rwanda'
    SAINTKITTSANDNEVIS = 'saintkittsandnevis'
    SAINTLUCIA = 'saintlucia'
    SAINTVINCENTANDGRENADINES = 'saintvincentandgrenadines'
    SALVADOR = 'salvador'
    SAMOA = 'samoa'
    SAOTOMEANDPRINCIPE = 'saotomeandprincipe'
    SAUDIARABIA = 'saudiarabia'
    SENEGAL = 'senegal'
    SERBIA = 'serbia'
    SEYCHELLES = 'seychelles'
    SIERRALEONE = 'sierraleone'
    SINGAPORE = 'singapore'
    SLOVAKIA = 'slovakia'
    SLOVENIA = 'slovenia'
    SOLOMONISLANDS = 'solomonislands'
    SOMALIA = 'somalia'
    SOUTHAFRICA = 'southafrica'
    SOUTHSUDAN = 'southsudan'
    SRILANKA = 'srilanka'
    SUDAN = 'sudan'
    SURINAME = 'suriname'
    SWAZILAND = 'swaziland'
    SWITZERLAND = 'switzerland'
    SYRIA = 'syria'
    TAIWAN = 'taiwan'
    TAJIKISTAN = 'tajikistan'
    TANZANIA = 'tanzania'
    THAILAND = 'thailand'
    TIT = 'tit'
    TOGO = 'togo'
    TONGA = 'tonga'
    TUNISIA = 'tunisia'
    TURKEY = 'turkey'
    TURKMENISTAN = 'turkmenistan'
    TURKSANDCAICOS = 'turksandcaicos'
    UAE = 'uae'
    UGANDA = 'uganda'
    URUGUAY = 'uruguay'
    UZBEKISTAN = 'uzbekistan'
    VENEZUELA = 'venezuela'
    VIRGINISLANDS = 'virginislands'
    YEMEN = 'yemen'
    ZAMBIA = 'zambia'
    ZIMBABWE = 'zimbabwe'
    DENMARK = 'denmark'
    KIRGHIZIA = 'kirghizia'
    TRINIDAD = 'trinidad'
    BOSNIA = 'bosnia'
    BRUNEI = 'brunei'
    ICELAND = 'iceland'
    MONACO = 'monaco'
    LEBANON = 'lebanon'
    PALESTINE = 'palestine'
    FIJI = 'fiji'
    SOUTHKOREA = 'southkorea'
    NORTHKOREA = 'northkorea'
    WESTERNSAHARA = 'westernsahara'
    JERSEY = 'jersey'
    BERMUDA = 'bermuda'
    MALTA = 'malta'
    POLAND = 'poland'
    SWEDEN = 'sweden'
    UNITED_KINGDOM = 'united_kingdom'
    UKRAINE = 'ukraine'
    PORTUGAL = 'portugal'
    SPAIN = 'spain'
    NETHERLANDS = 'netherlands'


class Operators:
    BEELINE = 'beeline'
    ROSTELECOM = 'rostelecom'
    COMVIQ = 'comviq'
    ACTIV = 'activ'
    YOTA = 'yota'
    DNA = 'dna'
    VIETNAMOBILE = 'vietnamobile'
    LYCAMOBILE = 'lycamobile'
    CHINA_MOBILE = 'china mobile'
    ORANGE = 'orange'
    ALTEL = 'altel'
    TELCEL = 'telcel'
    AXIS = 'axis'
    TELE2 = 'tele2'
    YOIGO = 'yoigo'
    THREE = 'three'
    TELIA = 'telia'
    MTT = 'mtt'
    TMOBILE = 'tmobile'
    LMT = 'lmt'
    LIFECELL = 'lifecell'
    MEGAFON = 'megafon'
    MTS = 'mts'
    LEBARA = 'lebara'
    KYIVSTAR = 'kyivstar'
    SMARTONE = 'smartone'
    CSL = 'csl'
    TELENOR = 'telenor'
    ELISA = 'elisa'
    VODAFONE = 'vodafone'
    UTEL = 'utel'
    LIFE = 'life'
    AKTIV = 'aktiv'

    ANY = 'any'


OPERATORS_COUNTRIES = \
{
    ActivatorName.SMS_ACTIVATE:
    {
        Countries.RUSSIA: [Operators.MEGAFON, Operators.MTS, Operators.BEELINE, Operators.TELE2, Operators.ROSTELECOM, Operators.ANY],
        Countries.UKRAINE: [Operators.KYIVSTAR, Operators.LIFE, Operators.UTEL, Operators.MTS, Operators.VODAFONE],
        Countries.KAZAKHSTAN: [Operators.TELE2, Operators.BEELINE, Operators.AKTIV, Operators.ALTEL],
    },

    ActivatorName.VAK_SMS:
    {
        Countries.ESTONIA: [Operators.ELISA, Operators.TELE2, Operators.TELIA],
        Countries.FINLAND: [Operators.DNA, Operators.ELISA],
        Countries.FRANCE: [Operators.LEBARA, Operators.LYCAMOBILE],
        Countries.GERMANY: [Operators.LYCAMOBILE],
        Countries.HONGKONG: [Operators.CHINA_MOBILE, Operators.CSL, Operators.SMARTONE, Operators.THREE],
        Countries.INDONESIA: [Operators.AXIS],
        Countries.KAZAKHSTAN: [Operators.ACTIV, Operators.ALTEL, Operators.BEELINE, Operators.TELE2],
        Countries.LATVIA: [Operators.LMT, Operators.TELE2],
        Countries.LITHUANIA: [Operators.TELE2],
        Countries.MEXICO: [Operators.TELCEL],
        Countries.NETHERLANDS: [Operators.LYCAMOBILE, Operators.LEBARA],
        Countries.POLAND: [Operators.ORANGE],
        Countries.PORTUGAL: [Operators.LYCAMOBILE, Operators.VODAFONE],
        Countries.RUSSIA: [
            Operators.BEELINE,
            Operators.LYCAMOBILE,
            Operators.MEGAFON,
            Operators.MTS,
            Operators.MTT,
            Operators.ROSTELECOM,
            Operators.TELE2,
            Operators.YOTA
        ],
        Countries.SPAIN: [Operators.LYCAMOBILE, Operators.YOIGO],
        Countries.SWEDEN: [Operators.COMVIQ, Operators.LYCAMOBILE, Operators.TELENOR],
        Countries.UKRAINE: [Operators.KYIVSTAR, Operators.LIFECELL, Operators.LYCAMOBILE, Operators.VODAFONE],
        Countries.UNITED_KINGDOM: [Operators.THREE, Operators.TMOBILE, Operators.VODAFONE],
        Countries.VIETNAM: [Operators.VIETNAMOBILE],
    }
}


REGIONS = RegionsList([
    Region(
        Countries.LATVIA,
        371,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '49'),
            ActivatorID(ActivatorName.FIVE_SIM, 'latvia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '371'),
            ActivatorID(ActivatorName.VAK_SMS, 'lv'),
        ]
    ),
    Region(
        Countries.LITHUANIA,
        370,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '44'),
            ActivatorID(ActivatorName.FIVE_SIM, 'lithuania'),
            ActivatorID(ActivatorName.ONLINE_SIM, '370'),
            ActivatorID(ActivatorName.VAK_SMS, 'lt'),
        ]
    ),
    Region(
        Countries.ESTONIA,
        372,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '34'),
            ActivatorID(ActivatorName.FIVE_SIM, 'estonia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '372'),
            ActivatorID(ActivatorName.VAK_SMS, 'ee'),
        ]
    ),
    Region(
        Countries.INDONESIA,
        62,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '6'),
            ActivatorID(ActivatorName.FIVE_SIM, 'indonesia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '62'),
            ActivatorID(ActivatorName.VAK_SMS, 'id'),
        ]
    ),
    Region(
        Countries.RUSSIA,
        7,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '0'),
            ActivatorID(ActivatorName.FIVE_SIM, 'russia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '7'),
            ActivatorID(ActivatorName.VAK_SMS, 'ru'),
            ActivatorID(ActivatorName.DROP_SMS, '0'),
        ]
    ),
    Region(
        Countries.GERMANY,
        49,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '43'),
            ActivatorID(ActivatorName.FIVE_SIM, 'germany'),
            ActivatorID(ActivatorName.ONLINE_SIM, '49'),
            ActivatorID(ActivatorName.VAK_SMS, 'de'),
        ]
    ),
    Region(
        Countries.KAZAKHSTAN,
        7,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '2'),
            ActivatorID(ActivatorName.FIVE_SIM, 'kazakhstan'),
            ActivatorID(ActivatorName.ONLINE_SIM, '77'),
            ActivatorID(ActivatorName.VAK_SMS, 'kz'),
        ]
    ),
    Region(
        Countries.FINLAND,
        358,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '163'),
            ActivatorID(ActivatorName.FIVE_SIM, 'finland'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, 'fi'),
        ]
    ),
    Region(
        Countries.INDIA,
        91,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '22'),
            ActivatorID(ActivatorName.FIVE_SIM, 'india'),
            ActivatorID(ActivatorName.ONLINE_SIM, '91'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CANADA,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '36'),
            ActivatorID(ActivatorName.FIVE_SIM, 'canada'),
            ActivatorID(ActivatorName.ONLINE_SIM, '1000'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.USA,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '187'),
            ActivatorID(ActivatorName.FIVE_SIM, 'usa'),
            ActivatorID(ActivatorName.ONLINE_SIM, '7'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.VIETNAM,
        84,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '10'),
            ActivatorID(ActivatorName.FIVE_SIM, 'vietnam'),
            ActivatorID(ActivatorName.ONLINE_SIM, '84'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.IVORYCOAST,
        225,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '27'),
            ActivatorID(ActivatorName.FIVE_SIM, 'ivorycoast'),
            ActivatorID(ActivatorName.ONLINE_SIM, '225'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NIGERIA,
        234,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '19'),
            ActivatorID(ActivatorName.FIVE_SIM, 'nigeria'),
            ActivatorID(ActivatorName.ONLINE_SIM, '234'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GHANA,
        233,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '38'),
            ActivatorID(ActivatorName.FIVE_SIM, 'ghana'),
            ActivatorID(ActivatorName.ONLINE_SIM, '233'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.PAKISTAN,
        92,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '66'),
            ActivatorID(ActivatorName.FIVE_SIM, 'pakistan'),
            ActivatorID(ActivatorName.ONLINE_SIM, '92'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.AFGHANISTAN,
        93,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '74'),
            ActivatorID(ActivatorName.FIVE_SIM, 'afghanistan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ALBANIA,
        355,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '155'),
            ActivatorID(ActivatorName.FIVE_SIM, 'albania'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ALGERIA,
        58,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '58'),
            ActivatorID(ActivatorName.FIVE_SIM, 'algeria'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ANGOLA,
        244,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '76'),
            ActivatorID(ActivatorName.FIVE_SIM, 'angola'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ANGUILLA,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '181'),
            ActivatorID(ActivatorName.FIVE_SIM, 'anguilla'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ANTIGUAANDBARBUDA,
        1268,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '169'),
            ActivatorID(ActivatorName.FIVE_SIM, 'antiguaandbarbuda'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ARGENTINA,
        54,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '39'),
            ActivatorID(ActivatorName.FIVE_SIM, 'argentina'),
            ActivatorID(ActivatorName.ONLINE_SIM, '54'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ARMENIA,
        374,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '148'),
            ActivatorID(ActivatorName.FIVE_SIM, 'armenia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ARUBA,
        297,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '179'),
            ActivatorID(ActivatorName.FIVE_SIM, 'aruba'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.AUSTRALIA,
        61,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '175'),
            ActivatorID(ActivatorName.FIVE_SIM, 'australia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.AUSTRIA,
        43,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '50'),
            ActivatorID(ActivatorName.FIVE_SIM, 'austria'),
            ActivatorID(ActivatorName.ONLINE_SIM, '43'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.AZERBAIJAN,
        994,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '35'),
            ActivatorID(ActivatorName.FIVE_SIM, 'azerbaijan'),
            ActivatorID(ActivatorName.ONLINE_SIM, '994'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BAHAMAS,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '122'),
            ActivatorID(ActivatorName.FIVE_SIM, 'bahamas'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BAHRAIN,
        973,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '145'),
            ActivatorID(ActivatorName.FIVE_SIM, 'bahrain'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BANGLADESH,
        880,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '60'),
            ActivatorID(ActivatorName.FIVE_SIM, 'bangladesh'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BARBADOS,
        1246,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '118'),
            ActivatorID(ActivatorName.FIVE_SIM, 'barbados'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BELARUS,
        375,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '51'),
            ActivatorID(ActivatorName.FIVE_SIM, 'belarus'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BELGIUM,
        32,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '82'),
            ActivatorID(ActivatorName.FIVE_SIM, 'belgium'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BELIZE,
        501,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '124'),
            ActivatorID(ActivatorName.FIVE_SIM, 'belize'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BENIN,
        229,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '120'),
            ActivatorID(ActivatorName.FIVE_SIM, 'benin'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BHUTANE,
        975,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '158'),
            ActivatorID(ActivatorName.FIVE_SIM, 'bhutane'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BIH,
        387,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, None),
            ActivatorID(ActivatorName.FIVE_SIM, 'bih'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BOLIVIA,
        591,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '92'),
            ActivatorID(ActivatorName.FIVE_SIM, 'bolivia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '591'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BOTSWANA,
        267,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '123'),
            ActivatorID(ActivatorName.FIVE_SIM, 'botswana'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BRAZIL,
        55,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '73'),
            ActivatorID(ActivatorName.FIVE_SIM, 'brazil'),
            ActivatorID(ActivatorName.ONLINE_SIM, '55'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BULGARIA,
        359,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '83'),
            ActivatorID(ActivatorName.FIVE_SIM, 'bulgaria'),
            ActivatorID(ActivatorName.ONLINE_SIM, '359'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BURKINAFASO,
        226,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '152'),
            ActivatorID(ActivatorName.FIVE_SIM, 'burkinafaso'),
            ActivatorID(ActivatorName.ONLINE_SIM, '226'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BURUNDI,
        257,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '119'),
            ActivatorID(ActivatorName.FIVE_SIM, 'burundi'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CAMBODIA,
        855,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '24'),
            ActivatorID(ActivatorName.FIVE_SIM, 'cambodia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CAMEROON,
        237,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '41'),
            ActivatorID(ActivatorName.FIVE_SIM, 'cameroon'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CAPEVERDE,
        238,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '186'),
            ActivatorID(ActivatorName.FIVE_SIM, 'capeverde'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CAYMANISLANDS,
        1345,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '170'),
            ActivatorID(ActivatorName.FIVE_SIM, 'caymanislands'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CHAD,
        235,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '42'),
            ActivatorID(ActivatorName.FIVE_SIM, 'chad'),
            ActivatorID(ActivatorName.ONLINE_SIM, '235'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CHILE,
        56,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '151'),
            ActivatorID(ActivatorName.FIVE_SIM, 'chile'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CHINA,
        86,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '3'),
            ActivatorID(ActivatorName.FIVE_SIM, 'china'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.COLOMBIA,
        57,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '33'),
            ActivatorID(ActivatorName.FIVE_SIM, 'colombia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '57'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.COMOROS,
        269,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '133'),
            ActivatorID(ActivatorName.FIVE_SIM, 'comoros'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CONGO,
        243,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '150'),
            ActivatorID(ActivatorName.FIVE_SIM, 'congo'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.COSTARICA,
        506,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '93'),
            ActivatorID(ActivatorName.FIVE_SIM, 'costarica'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CROATIA,
        385,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '45'),
            ActivatorID(ActivatorName.FIVE_SIM, 'croatia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CUBA,
        53,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '113'),
            ActivatorID(ActivatorName.FIVE_SIM, 'cuba'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CYPRUS,
        357,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '77'),
            ActivatorID(ActivatorName.FIVE_SIM, 'cyprus'),
            ActivatorID(ActivatorName.ONLINE_SIM, '357'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.CZECH,
        420,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '63'),
            ActivatorID(ActivatorName.FIVE_SIM, 'czech'),
            ActivatorID(ActivatorName.ONLINE_SIM, '420'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.DJIBOUTI,
        253,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '168'),
            ActivatorID(ActivatorName.FIVE_SIM, 'djibouti'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.DOMINICA,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '126'),
            ActivatorID(ActivatorName.FIVE_SIM, 'dominica'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.DOMINICANA,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '109'),
            ActivatorID(ActivatorName.FIVE_SIM, 'dominicana'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.DRCONGO,
        243,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, 18),
            ActivatorID(ActivatorName.FIVE_SIM, 'drcongo'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.EASTTIMOR,
        670,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '91'),
            ActivatorID(ActivatorName.FIVE_SIM, 'easttimor'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ECUADOR,
        593,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '105'),
            ActivatorID(ActivatorName.FIVE_SIM, 'ecuador'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.EGYPT,
        20,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '21'),
            ActivatorID(ActivatorName.FIVE_SIM, 'egypt'),
            ActivatorID(ActivatorName.ONLINE_SIM, '20'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ENGLAND,
        44,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '16'),
            ActivatorID(ActivatorName.FIVE_SIM, 'england'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.EQUATORIALGUINEA,
        240,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '167'),
            ActivatorID(ActivatorName.FIVE_SIM, 'equatorialguinea'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ERITREA,
        291,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '176'),
            ActivatorID(ActivatorName.FIVE_SIM, 'eritrea'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ETHIOPIA,
        251,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '71'),
            ActivatorID(ActivatorName.FIVE_SIM, 'ethiopia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.FRANCE,
        33,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '78'),
            ActivatorID(ActivatorName.FIVE_SIM, 'france'),
            ActivatorID(ActivatorName.ONLINE_SIM, '33'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.FRENCHGUIANA,
        594,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '162'),
            ActivatorID(ActivatorName.FIVE_SIM, 'frenchguiana'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GABON,
        241,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '154'),
            ActivatorID(ActivatorName.FIVE_SIM, 'gabon'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GAMBIA,
        220,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '28'),
            ActivatorID(ActivatorName.FIVE_SIM, 'gambia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GEORGIA,
        995,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '128'),
            ActivatorID(ActivatorName.FIVE_SIM, 'georgia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '995'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GREECE,
        30,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '129'),
            ActivatorID(ActivatorName.FIVE_SIM, 'greece'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GRENADA,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '127'),
            ActivatorID(ActivatorName.FIVE_SIM, 'grenada'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GUADELOUPE,
        590,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '160'),
            ActivatorID(ActivatorName.FIVE_SIM, 'guadeloupe'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GUATEMALA,
        502,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '94'),
            ActivatorID(ActivatorName.FIVE_SIM, 'guatemala'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GUINEA,
        224,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '68'),
            ActivatorID(ActivatorName.FIVE_SIM, 'guinea'),
            ActivatorID(ActivatorName.ONLINE_SIM, '224'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GUINEABISSAU,
        245,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '130'),
            ActivatorID(ActivatorName.FIVE_SIM, 'guineabissau'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.GUYANA,
        592,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '131'),
            ActivatorID(ActivatorName.FIVE_SIM, 'guyana'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.HAITI,
        509,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '26'),
            ActivatorID(ActivatorName.FIVE_SIM, 'haiti'),
            ActivatorID(ActivatorName.ONLINE_SIM, '509'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.HONDURAS,
        504,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '88'),
            ActivatorID(ActivatorName.FIVE_SIM, 'honduras'),
            ActivatorID(ActivatorName.ONLINE_SIM, '504'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.HONGKONG,
        852,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '14'),
            ActivatorID(ActivatorName.FIVE_SIM, 'hongkong'),
            ActivatorID(ActivatorName.ONLINE_SIM, '852'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.HUNGARY,
        36,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '84'),
            ActivatorID(ActivatorName.FIVE_SIM, 'hungary'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.IRAN,
        98,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '57'),
            ActivatorID(ActivatorName.FIVE_SIM, 'iran'),
            ActivatorID(ActivatorName.ONLINE_SIM, '98'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.IRAQ,
        964,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '47'),
            ActivatorID(ActivatorName.FIVE_SIM, 'iraq'),
            ActivatorID(ActivatorName.ONLINE_SIM, '964'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.IRELAND,
        353,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '23'),
            ActivatorID(ActivatorName.FIVE_SIM, 'ireland'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ISRAEL,
        972,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '13'),
            ActivatorID(ActivatorName.FIVE_SIM, 'israel'),
            ActivatorID(ActivatorName.ONLINE_SIM, '972'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ITALY,
        39,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '86'),
            ActivatorID(ActivatorName.FIVE_SIM, 'italy'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.JAMAICA,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '103'),
            ActivatorID(ActivatorName.FIVE_SIM, 'jamaica'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.JAPAN,
        81,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '182'),
            ActivatorID(ActivatorName.FIVE_SIM, 'japan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.JORDAN,
        962,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '116'),
            ActivatorID(ActivatorName.FIVE_SIM, 'jordan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.KENYA,
        254,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '8'),
            ActivatorID(ActivatorName.FIVE_SIM, 'kenya'),
            ActivatorID(ActivatorName.ONLINE_SIM, '254'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.KUWAIT,
        965,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '100'),
            ActivatorID(ActivatorName.FIVE_SIM, 'kuwait'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.KYRGYZSTAN,
        996,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '11'),
            ActivatorID(ActivatorName.FIVE_SIM, 'kyrgyzstan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.LAOS,
        856,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '25'),
            ActivatorID(ActivatorName.FIVE_SIM, 'laos'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.LESOTHO,
        266,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '136'),
            ActivatorID(ActivatorName.FIVE_SIM, 'lesotho'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.LIBERIA,
        231,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '135'),
            ActivatorID(ActivatorName.FIVE_SIM, 'liberia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.LIBYA,
        218,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '102'),
            ActivatorID(ActivatorName.FIVE_SIM, 'libya'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.LUXEMBOURG,
        352,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '165'),
            ActivatorID(ActivatorName.FIVE_SIM, 'luxembourg'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MACAU,
        853,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '20'),
            ActivatorID(ActivatorName.FIVE_SIM, 'macau'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MADAGASCAR,
        17,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '17'),
            ActivatorID(ActivatorName.FIVE_SIM, 'madagascar'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MALAWI,
        265,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '137'),
            ActivatorID(ActivatorName.FIVE_SIM, 'malawi'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MALAYSIA,
        60,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '7'),
            ActivatorID(ActivatorName.FIVE_SIM, 'malaysia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MALDIVES,
        960,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '159'),
            ActivatorID(ActivatorName.FIVE_SIM, 'maldives'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MALI,
        223,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '69'),
            ActivatorID(ActivatorName.FIVE_SIM, 'mali'),
            ActivatorID(ActivatorName.ONLINE_SIM, '223'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MAURITANIA,
        222,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '114'),
            ActivatorID(ActivatorName.FIVE_SIM, 'mauritania'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MAURITIUS,
        230,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '157'),
            ActivatorID(ActivatorName.FIVE_SIM, 'mauritius'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MEXICO,
        52,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '54'),
            ActivatorID(ActivatorName.FIVE_SIM, 'mexico'),
            ActivatorID(ActivatorName.ONLINE_SIM, '52'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MOLDOVA,
        373,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '85'),
            ActivatorID(ActivatorName.FIVE_SIM, 'moldova'),
            ActivatorID(ActivatorName.ONLINE_SIM, '373'),
            ActivatorID(ActivatorName.VAK_SMS, 'md'),
        ]
    ),
    Region(
        Countries.MONGOLIA,
        976,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '72'),
            ActivatorID(ActivatorName.FIVE_SIM, 'mongolia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '976'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MONTENEGRO,
        382,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '171'),
            ActivatorID(ActivatorName.FIVE_SIM, 'montenegro'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MONTSERRAT,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '180'),
            ActivatorID(ActivatorName.FIVE_SIM, 'montserrat'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MOROCCO,
        212,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '37'),
            ActivatorID(ActivatorName.FIVE_SIM, 'morocco'),
            ActivatorID(ActivatorName.ONLINE_SIM, '212'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MOZAMBIQUE,
        258,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '80'),
            ActivatorID(ActivatorName.FIVE_SIM, 'mozambique'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MYANMAR,
        95,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '5'),
            ActivatorID(ActivatorName.FIVE_SIM, 'myanmar'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NAMIBIA,
        264,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '138'),
            ActivatorID(ActivatorName.FIVE_SIM, 'namibia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NEPAL,
        977,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '81'),
            ActivatorID(ActivatorName.FIVE_SIM, 'nepal'),
            ActivatorID(ActivatorName.ONLINE_SIM, '977'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NEWCALEDONIA,
        687,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '185'),
            ActivatorID(ActivatorName.FIVE_SIM, 'newcaledonia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NEWZEALAND,
        64,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '67'),
            ActivatorID(ActivatorName.FIVE_SIM, 'newzealand'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NICARAGUA,
        505,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '90'),
            ActivatorID(ActivatorName.FIVE_SIM, 'nicaragua'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NIGER,
        227,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '139'),
            ActivatorID(ActivatorName.FIVE_SIM, 'niger'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NORTHMACEDONIA,
        389,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '183'),
            ActivatorID(ActivatorName.FIVE_SIM, 'northmacedonia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NORWAY,
        47,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '174'),
            ActivatorID(ActivatorName.FIVE_SIM, 'norway'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.OMAN,
        968,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '107'),
            ActivatorID(ActivatorName.FIVE_SIM, 'oman'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.PANAMA,
        507,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '112'),
            ActivatorID(ActivatorName.FIVE_SIM, 'panama'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.PAPUANEWGUINEA,
        675,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '79'),
            ActivatorID(ActivatorName.FIVE_SIM, 'papuanewguinea'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.PARAGUAY,
        595,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '87'),
            ActivatorID(ActivatorName.FIVE_SIM, 'paraguay'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.PERU,
        51,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '65'),
            ActivatorID(ActivatorName.FIVE_SIM, 'peru'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.PHILIPPINES,
        63,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '4'),
            ActivatorID(ActivatorName.FIVE_SIM, 'philippines'),
            ActivatorID(ActivatorName.ONLINE_SIM, '63'),
            ActivatorID(ActivatorName.VAK_SMS, 'ph'),
        ]
    ),
    Region(
        Countries.PUERTORICO,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '97'),
            ActivatorID(ActivatorName.FIVE_SIM, 'puertorico'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.QATAR,
        974,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '111'),
            ActivatorID(ActivatorName.FIVE_SIM, 'qatar'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.REUNION,
        262,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '146'),
            ActivatorID(ActivatorName.FIVE_SIM, 'reunion'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ROMANIA,
        40,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '32'),
            ActivatorID(ActivatorName.FIVE_SIM, 'romania'),
            ActivatorID(ActivatorName.ONLINE_SIM, '40'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.RWANDA,
        250,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '140'),
            ActivatorID(ActivatorName.FIVE_SIM, 'rwanda'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SAINTKITTSANDNEVIS,
        1869,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '134'),
            ActivatorID(ActivatorName.FIVE_SIM, 'saintkittsandnevis'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SAINTLUCIA,
        1758,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '164'),
            ActivatorID(ActivatorName.FIVE_SIM, 'saintlucia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SAINTVINCENTANDGRENADINES,
        1784,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '166'),
            ActivatorID(ActivatorName.FIVE_SIM, 'saintvincentandgrenadines'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SALVADOR,
        503,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '101'),
            ActivatorID(ActivatorName.FIVE_SIM, 'salvador'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SAMOA,
        685,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '198'),
            ActivatorID(ActivatorName.FIVE_SIM, 'samoa'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SAOTOMEANDPRINCIPE,
        239,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '178'),
            ActivatorID(ActivatorName.FIVE_SIM, 'saotomeandprincipe'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SAUDIARABIA,
        966,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '53'),
            ActivatorID(ActivatorName.FIVE_SIM, 'saudiarabia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SENEGAL,
        221,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '61'),
            ActivatorID(ActivatorName.FIVE_SIM, 'senegal'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SERBIA,
        381,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '29'),
            ActivatorID(ActivatorName.FIVE_SIM, 'serbia'),
            ActivatorID(ActivatorName.ONLINE_SIM, '381'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SEYCHELLES,
        248,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '184'),
            ActivatorID(ActivatorName.FIVE_SIM, 'seychelles'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SIERRALEONE,
        232,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '115'),
            ActivatorID(ActivatorName.FIVE_SIM, 'sierraleone'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SINGAPORE,
        65,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '196'),
            ActivatorID(ActivatorName.FIVE_SIM, 'singapore'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SLOVAKIA,
        421,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '141'),
            ActivatorID(ActivatorName.FIVE_SIM, 'slovakia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SLOVENIA,
        386,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '59'),
            ActivatorID(ActivatorName.FIVE_SIM, 'slovenia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SOLOMONISLANDS,
        677,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '193'),
            ActivatorID(ActivatorName.FIVE_SIM, 'solomonislands'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SOMALIA,
        252,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '149'),
            ActivatorID(ActivatorName.FIVE_SIM, 'somalia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SOUTHAFRICA,
        27,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '31'),
            ActivatorID(ActivatorName.FIVE_SIM, 'southafrica'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SOUTHSUDAN,
        211,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '177'),
            ActivatorID(ActivatorName.FIVE_SIM, 'southsudan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SRILANKA,
        94,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '64'),
            ActivatorID(ActivatorName.FIVE_SIM, 'srilanka'),
            ActivatorID(ActivatorName.ONLINE_SIM, '94'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SUDAN,
        249,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '98'),
            ActivatorID(ActivatorName.FIVE_SIM, 'sudan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SURINAME,
        597,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '142'),
            ActivatorID(ActivatorName.FIVE_SIM, 'suriname'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SWAZILAND,
        268,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '106'),
            ActivatorID(ActivatorName.FIVE_SIM, 'swaziland'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SWITZERLAND,
        41,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '173'),
            ActivatorID(ActivatorName.FIVE_SIM, 'switzerland'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SYRIA,
        963,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '110'),
            ActivatorID(ActivatorName.FIVE_SIM, 'syria'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TAIWAN,
        886,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '55'),
            ActivatorID(ActivatorName.FIVE_SIM, 'taiwan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TAJIKISTAN,
        992,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '143'),
            ActivatorID(ActivatorName.FIVE_SIM, 'tajikistan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TANZANIA,
        255,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '9'),
            ActivatorID(ActivatorName.FIVE_SIM, 'tanzania'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.THAILAND,
        66,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '52'),
            ActivatorID(ActivatorName.FIVE_SIM, 'thailand'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TIT,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, None),
            ActivatorID(ActivatorName.FIVE_SIM, 'tit'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TOGO,
        228,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '99'),
            ActivatorID(ActivatorName.FIVE_SIM, 'togo'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TONGA,
        676,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '197'),
            ActivatorID(ActivatorName.FIVE_SIM, 'tonga'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TUNISIA,
        216,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '89'),
            ActivatorID(ActivatorName.FIVE_SIM, 'tunisia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TURKEY,
        90,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '62'),
            ActivatorID(ActivatorName.FIVE_SIM, 'turkey'),
            ActivatorID(ActivatorName.ONLINE_SIM, '90'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TURKMENISTAN,
        993,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '161'),
            ActivatorID(ActivatorName.FIVE_SIM, 'turkmenistan'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TURKSANDCAICOS,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, None),
            ActivatorID(ActivatorName.FIVE_SIM, 'turksandcaicos'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.UAE,
        971,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '95'),
            ActivatorID(ActivatorName.FIVE_SIM, 'uae'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.UGANDA,
        256,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '75'),
            ActivatorID(ActivatorName.FIVE_SIM, 'uganda'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.URUGUAY,
        598,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '156'),
            ActivatorID(ActivatorName.FIVE_SIM, 'uruguay'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.UZBEKISTAN,
        998,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '40'),
            ActivatorID(ActivatorName.FIVE_SIM, 'uzbekistan'),
            ActivatorID(ActivatorName.ONLINE_SIM, '998'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.VENEZUELA,
        58,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '70'),
            ActivatorID(ActivatorName.FIVE_SIM, 'venezuela'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.VIRGINISLANDS,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, None),
            ActivatorID(ActivatorName.FIVE_SIM, 'virginislands'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.YEMEN,
        967,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '30'),
            ActivatorID(ActivatorName.FIVE_SIM, 'yemen'),
            ActivatorID(ActivatorName.ONLINE_SIM, '967'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ZAMBIA,
        260,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '147'),
            ActivatorID(ActivatorName.FIVE_SIM, 'zambia'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ZIMBABWE,
        263,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '96'),
            ActivatorID(ActivatorName.FIVE_SIM, 'zimbabwe'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.DENMARK,
        45,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '172'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, '45'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.KIRGHIZIA,
        996,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, None),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, '996'),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.TRINIDAD,
        868,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '104'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BOSNIA,
        387,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '108'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BRUNEI,
        673,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '121'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.ICELAND,
        354,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '132'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MONACO,
        377,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '144'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.LEBANON,
        961,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '153'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.PALESTINE,
        970,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '188'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.FIJI,
        679,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '189'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.SOUTHKOREA,
        82,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '190'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.NORTHKOREA,
        850,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '191'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.WESTERNSAHARA,
        212,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '192'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.JERSEY,
        44,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '194'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.BERMUDA,
        1,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '195'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.MALTA,
        356,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '199'),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, None),
        ]
    ),
    Region(
        Countries.POLAND,
        48,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '15'),
            ActivatorID(ActivatorName.FIVE_SIM, 'poland'),
            ActivatorID(ActivatorName.ONLINE_SIM, '48'),
            ActivatorID(ActivatorName.VAK_SMS, 'pl'),
        ]
    ),
    Region(
        Countries.SWEDEN,
        46,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '46'),
            ActivatorID(ActivatorName.FIVE_SIM, 'sweden'),
            ActivatorID(ActivatorName.ONLINE_SIM, '46'),
            ActivatorID(ActivatorName.VAK_SMS, 'se'),
        ]
    ),
    Region(
        Countries.UNITED_KINGDOM,
        44,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, None),
            ActivatorID(ActivatorName.FIVE_SIM, None),
            ActivatorID(ActivatorName.ONLINE_SIM, '44'),
            ActivatorID(ActivatorName.VAK_SMS, 'gb'),
        ]
    ),
    Region(
        Countries.UKRAINE,
        380,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '1'),
            ActivatorID(ActivatorName.FIVE_SIM, 'ukraine'),
            ActivatorID(ActivatorName.ONLINE_SIM, '380'),
            ActivatorID(ActivatorName.VAK_SMS, 'ua'),
        ]
    ),
    Region(
        Countries.PORTUGAL,
        351,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '117'),
            ActivatorID(ActivatorName.FIVE_SIM, 'portugal'),
            ActivatorID(ActivatorName.ONLINE_SIM, None),
            ActivatorID(ActivatorName.VAK_SMS, 'pt'),
        ]
    ),
    Region(
        Countries.SPAIN,
        34,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '56'),
            ActivatorID(ActivatorName.FIVE_SIM, 'spain'),
            ActivatorID(ActivatorName.ONLINE_SIM, '34'),
            ActivatorID(ActivatorName.VAK_SMS, 'es'),
        ]
    ),
    Region(
        Countries.NETHERLANDS,
        31,
        [
            ActivatorID(ActivatorName.SMS_ACTIVATE, '48'),
            ActivatorID(ActivatorName.FIVE_SIM, 'netherlands'),
            ActivatorID(ActivatorName.ONLINE_SIM, '31'),
            ActivatorID(ActivatorName.VAK_SMS, 'nl'),
        ]
    ),
])
