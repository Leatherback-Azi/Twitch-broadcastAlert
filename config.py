class config:
    # Buzzer Freq by Sound
    DO = 1046
    DO_SHARP = 1108
    RE = 1174
    RE_SHARP = 1244
    MI = 1308
    PA = 1396
    PA_SHARP = 1479
    SOL = 1567
    SOL_SHARP = 1661
    RA = 1760
    RA_SHARP = 1864
    SI = 1975
    DO_HIGH = 2093

    ##### About Configuration #####
    ## VALUE MUST BE 'False' IN PRODUCTION! ##
    DEBUG = False

    ##### About RPI #####
    # BCM or BOARD
    PIN_CALL = 'BCM'
    # Pin out
    LED_1_OUT = 17      # LED Pin out
    BUZZER_1_OUT = 27   # Buzzer Pin out
    # Sound Freq
    BUZZER_SCALE_1 = [MI, MI, MI, MI, MI, RE, DO, SI, DO]
    BUZZER_PLAYTIME_1 = [0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.4, 0.4]
    BUZZER_SLEEPTIME_1 = [0.05, 0.05, 0.05, 0.05, 0.3, 0.05, 0.05, 0.05, 0]

    ##### About API #####
    # Django/Twitch API Server For Debug.
    DEBUG_URL = 'http://192.168.0.23:8000/kraken/'
    URL = 'https://api.twitch.tv/kraken/'

    # Twitch API Headers
    HEADERS = {
        'Client-ID': 'YOUR_TWITCH_API_CLI',
        'Accept': 'application/vnd.twitchtv.v5+json',
    }

    # BroadCaster ID
    NAME_1 = 'dkwl025'

    # Others
    REFRESH_RATE = 5        # Secs
