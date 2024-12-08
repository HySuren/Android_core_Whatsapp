import os
import random
import subprocess


import uiautomator2 as u2

import config

def change_memory(serial):
    random_size = random.randint(500, 5000)
    subprocess.run(
        f'adb -s {serial} shell "rm {config.PHONE_TMP_FOLDER}/clear_file"',
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    )
    subprocess.run(
        f'adb -s {serial} shell "fallocate -l {random_size}M {config.PHONE_TMP_FOLDER}/clear_file"',
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    )


def install_random_apps(device: u2.Device, apps_amount=3):
    for app in list(set(random.choices(os.listdir('apk/random_apps'), k=apps_amount))):
        # subprocess.call(f"adb -s {device.serial} install -d apk/random_apps/{app}", shell=True, stdout=subprocess.DEVNULL)
        device.app_install('apk/random_apps/' + app)


def uninstall_random_apps(device: u2.Device):
    apks = {'com.newsblur', 'com.zwh.flip.clock', 'net.piaohong.newsgroup', 'com.cocoswing.tedict', 'com.euronews.express', 'ru.boloid.lifenews', 'com.dilstudio.easyrecipes', 'com.appmindlab.nano', 'com.voicenotebook.voicenotebook', 'com.tikamori.trickme', 'com.sourcecodetrans.russianuzbek', 'com.atnsoft.calculator.free', 'com.axidep.wordbook', 'com.thomasokken.free42', 'com.xzcompany.alcometr', 'com.timy.alarmclock', 'weatherradar.livemaps.free', 'ru.fourpda.client', 'org.redwid.android.videorss', 'ai.tveyni.just_eatby', 'ru.involta.radio', 'com.axidep.poliglot', 'com.crystalmissions.noradio', 'com.issuu.android.app', 'org.mmin.handycalc', 'ak.alizandro.smartaudiobookplayer', 'com.app.technoblog', 'com.info.weather.forecast', 'com.resonancelab.unrar', 'org.ab.x48', 'pro.comparator', 'cc.dict.dictcc', 'ru.rambler.media_app', 'com.fenchtose.reflog', 'com.zedtema.android.radio', 'com.elasthink.lyricstraining', 'com.rarlab.rar', 'kz.tengrinews', 'ru.vodnouho.android.yourday', 'com.gavdulskiy.roman.trashbox', 'com.kudago.android', 'com.dmitsoft.tonegenerator', 'gonemad.gmmp', 'sk.michalec.SimpleDigiClockWidget', 'org.androworks.klara', 'ru.mail.pulseandroid', 'com.sonyericsson.digitalclockwidget2', 'org.xbasoft.mubarometer', 'com.agilesoftresource', 'media.mp3player.musicplayer', 'audioplayer.free.music.player', 'com.ihandysoft.alarmclock', 'com.weawow', 'ru.my1.mytrue.mypoints', 'com.night.clock.nightclock.live.wallpaper.day.night.analog.digitalclock', 'ru.mail.mailnews', 'com.lapay.laplayer', 'com.dencreak.engwordstop', 'com.ba.fractioncalculator', 'com.noinnion.android.greader.reader', 'jp.ne.kutu.Panecal', 'com.romankutzencko.legacyshield', 'com.scand.smartreader', 'eir.synaxarion.ru', 'de.danoeh.antennapod', 'ru.kaomoji.kaomojiapp', 'free.translate.all.language.translator', 'com.vertaler.ruen', 'brain.reaction.concentration'}
    apks_to_delete = apks & set(device.app_list())
    for app in list(apks_to_delete):
        device.app_uninstall(app)
