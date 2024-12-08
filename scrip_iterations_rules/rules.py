from core.activity import AppActivity, ActivityMethodDict, ANY, AppActivityWithLikeText
from scrip_iterations_rules.activity_methods import *


OFFER_TO_EDIT_NUMBER = 'You entered the phone number:\n\n{phone_replaced}\n\nIs this OK, or would you like to edit the number?'
PHONE_BANNED = '{phone_replaced}\n\nis banned from using WhatsApp. Contact support for help.'
UNABLE_CONNECT_PLEASE_CHECK = 'Unable to connect. Please check that you are connected to the Internet and try again.\n\nPlease reboot your phone if your connection problem persists.'
YOU_RECENTLY_CONNECTED = 'You recently connected. Please wait'
CHECK_YOUR_NUMBER = "We couldn't send an SMS to your number. Please check your number and try again in 1 hour."
WHATSAPP_UNAVAILABLE = "WhatsApp is temporarily unavailable. Please try again in 5 minutes."
PHONE_NO_LONGER_REG = "Your phone number is no longer registered with WhatsApp on this phone. This might be because you registered it on another phone.\n\nIf you didn't do this, verify your phone number to log back into your account."
OFFER_T0_ALLOW_WA = 'To easily send messages and photos to friends and family, allow WhatsApp to access your contacts, photos and other media.'
ALLOW_CONTACTS = 'Allow WhatsApp to access your contacts?'
ALLOW_PHOTOS = 'Allow WhatsApp to access photos and media on your device?'
ALLOW_CALLS = 'Allow WhatsApp to record audio?'
ALLOW_NOTIFICATIONS = 'Allow WhatsApp to send you notifications?'
ALLOW_AUDIO = 'Allow WhatsApp to access music and audio on this device?'
ALLOW_VIDEOS = 'Allow WhatsApp to access photos and videos on this device?'
NEW_BACKUP_PERMISSION = 'If you previously backed up to Google storage and want to restore it, give WhatsApp permission to check your Google account for backups.'
BACKUP_PERMISSION = 'If you previously backed up to Google Drive and want to restore it, give WhatsApp permission to check your Google account for backups.'
UNABLE_CONNECT_TRY_AGAIN = 'Unable to connect. Please try again later.'
NOT_VALID = "The phone number {phone_replaced} isn't on WhatsApp."
NOT_VALID_NUMBER = '{phone_replaced}\nis not a valid mobile number for the country'
DELETE_CHAT = 'Delete chat with "{phone_replaced}"?'
DELETE_CHAT2 = 'Delete chat with "{phone_replaced}"?\nYou have 1 unsent message in this chat.'
DELETE_CHAT3 = 'Delete this chat?'
COULDNT_FIND_PHONE = "Couldn't look up phone number {phone_replaced}. Try again later."
SWITCHNG_BUSINESS_PATTERN = "Switching to WhatsApp Messenger will delete all of your business information\n\nOnly your messages and media will move. You will permanently lose your:"
SWITCHNG_BUSINESS = "Switching to WhatsApp Messenger will delete all of your business information\n\nOnly your messages and media will move. You will permanently lose your:\n\n- Catalog and items\n- Greeting and Away messages\n- Labels\n\nBy switching, you confirm you approve deletion of your information.\n\nOr you can edit the number.\n\n{phone_replaced}"
SWITCHNG_BUSINESS2 = "This phone number is currently registered with WhatsApp Messenger and can't be used in WhatsApp Business at the same time.\n\nWould you like to continue and move this phone number to WhatsApp Business or would you like to edit the number?\n\n{phone_replaced}"
DEVICE_LOGIN = "Device login code detected"
NEW_WEB = "Now use WhatsApp without keeping your phone online."
CONNECT_WIFI = "Connect to WiFi to continue"
CHECK_INTERNET = "Couldn't log in. Check your phone's Internet connection and scan the QR code again."
COULDNT_LINK = "Couldn't link device"
COULDNT_CALL = "We couldn't call your number. Please check your number and try again"
REQUESTING_CALL = "Requesting a call..."
YOU_GUESSED = "You have guessed too many times.\n\nPlease check with your mobile provider that you can receive SMS and phone calls.\n\nPlease wait for a new code to be sent.\n\nTry again after"
YOU_HAVE_REQUESTED = "You have requested your code too many times.\n\nPlease check with your mobile provider that you can receive SMS and phone calls.\n\nPlease enter the code we send you.\n\nTry again after"
YOU_TRIED = 'You tried requesting code to other phone too many times. To verify, tap "Send SMS".'
LINK_FB = "Your Business profile can now link to your Facebook and Instagram"
VERIFY_YOUR_ACCOUNT = 'Verify your account'
SENDING_CODE = 'Sending code...'
CODE_VERIFIED = 'Code verified'
VERIFY_NUMBER = 'Verify phone number'
VERIFY_YOUR_NUMBER = 'Verify your number'
VERIFY_NUMBER_ANOTHER_WAY = 'Verify your phone number another way'
TRIED_MANY_TIMES = 'You tried SMS verification too many times. To verify, tap "Call me".'
CONTACTS_AND_MEDIA = 'Contacts and media'
RESTORE_BACKUP = 'Restore a backup'
LOOKING_BACKUPS = 'Looking for backups'
UPDATE_WA = 'Update WhatsApp'
ENTER_YOUR_NUMBER = 'Enter your phone number'
PLEASE_CONTACT_CUSTOMER_SUPPORT = 'Sorry, an unrecoverable error has occurred. Please contact customer support for assistance.'

CODE_REQUESTED = 'WhatsApp Registration Code Requested'
ENTER_PIN = 'Enter your two-step verification PIN'
START_CALL = 'Start voice call?'
MANY_ATTEMPTS = 'Too many attempts'
IS_CORRECT_NUMBER = 'Is this the correct number?'
END_WHATSAPP_CALL = 'Placing this call will end your WhatsApp call.'
SURE_INTERNET_CONNECTION = 'Couldn\'t place call. Make sure your device has an Internet connection and try again.'
PLACE_WHATSAPP_CALL = "To place a WhatsApp call, first turn off Airplane mode."
JUST_ANSWERED_CALL = "just answered your call. Do you want to continue the call?"

CONNECTING = 'Connecting...'
REQUESTING_AN_SMS = 'Requesting an SMS...'
REQUESTING_AN_SMS_INSTEAD = 'Requesting SMS instead...'
REQUESTING_CODE = 'Requesting code...'
VERIFYING = 'Verifying...'
VERIFYING_NUMBER = 'Verifying your number'
VERIFICATION_COMPLETE = 'Verification complete'
LOADING = 'Loading...'
APPLYING_SETTINGS = 'Applying settings...'
SEARCHING = 'Searching...'
UPDATING = 'Updating...'
LOGGING_IN = 'Logging in...'
PLEASE_WAIT = 'Please wait a moment'
NEW = 'NEW'
NEW2 = 'New'
DOCUMENT = 'Document'
ALLOW_DRONY = 'Allow Drony to access this device’s location?'
NO_ITERNET = 'Unable to connect. Please check that you are connected to the Internet and try again.\n\nPlease reboot your device if your connection problem continues.'

PARTICIPANT_CANNOT_BE_ADDED = "This participant can't be added to the community. You can invite them privately to join this group through its invite link."
YOU_CANT_ADD_PARTICIPANTS = "You can't add participants because you're not a participant."
INVALID_PHOTO_RESOLUTION = "This photo is too small. Please select a photo with height and width of at least 192 pixels."


ACTIVITY__METHODS_DICT = ActivityMethodDict({

    # ЗВОНКИ
    AppActivity(package=ANY, activity_name=ANY, popup_exists=ANY, text=ANY, is_call=True): handle_call,
    # ОКНА СИСТЕМЫ
    # AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text='Sorry, an unrecoverable error has occurred. Please contact customer support for assistance.'): handle_go_back, STOP_ITERRATION TODO обработать корректно
    AppActivity(package='com.sec.android.app.launcher', activity_name='.activities.LauncherActivity'): reset_wa,
    AppActivity(package='com.google.android.permissioncontroller', activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity', popup_exists=True, text=ANY): allow_permission,
    # AppActivity(package='com.google.android.permissioncontroller', activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity', popup_exists=True, text=ALLOW_CONTACTS): allow_permission,
    # AppActivity(package='com.google.android.permissioncontroller', activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity', popup_exists=True, text=ALLOW_PHOTOS): allow_permission,
    # AppActivity(package='com.google.android.permissioncontroller', activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity', popup_exists=True, text=ALLOW_CALLS): allow_permission,
    # AppActivity(package='com.google.android.permissioncontroller', activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity', popup_exists=True, text=ALLOW_NOTIFICATIONS): allow_permission,
    # AppActivity(package='com.google.android.permissioncontroller', activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity', popup_exists=True, text=ALLOW_AUDIO): allow_permission,
    # AppActivity(package='com.google.android.permissioncontroller', activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity', popup_exists=True, text=ALLOW_VIDEOS): allow_permission,
    AppActivity(package='com.android.stk2', activity_name='.StkDialogActivity', popup_exists=True, text=ANY): disagree_popup,
    AppActivity(package='com.samsung.android.app.contacts', activity_name='com.samsung.android.contacts.legacy.vcard.ImportVCardPreviewActivity'): import_contacts,
    AppActivity(package='com.wssyncmldm', activity_name='com.idm.fotaagent.enabler.ui.installconfirm.InstallConfirmActivity'): handle_go_back,
    # AppActivity(package='com.android.server.telecom', activity_name='.ui.ConfirmCallDialogActivity', popup_exists=True, text=END_WHATSAPP_CALL): end_whatsapp_call,

    # ОКНА WHATSAPP
    AppActivity(package='com.whatsapp', activity_name='.registration.phonenumberentry.RegisterPhone'): enter_reg_phone,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterName', popup_exists=True, text='Looking for backups'): do_nothing,
    AppActivity(package=ANY, activity_name=ANY, popup_exists=True, text=UPDATE_WA): handle_go_back,
    AppActivity(package='com.whatsapp', activity_name='.registration.phonenumberentry.RegisterPhone', popup_exists=True, text=NO_ITERNET): handle_stop_iteration,
    # AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber', popup_exists=True, text="Code verified"): do_nothing, ??? обработать как клик ОК TODO обработать корректно
    AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber', popup_exists=True, text=PLEASE_CONTACT_CUSTOMER_SUPPORT): handle_stop_iteration,
    AppActivity(package='com.whatsapp', activity_name='.registration.phonenumberentry.RegisterPhone', popup_exists=True, text="Sending code...", is_loading=True): do_nothing,
    # AppActivity(package='com.whatsapp', activity_name='.backup.google.RestoreFromBackupActivity', popup_exists=True, text="If you previously backed up to Google storage and want to restore it, give WhatsApp permission to check your Google account for backups."): skip_backup, ПОймать активность и проверить как работает TODO обработать корректно
    AppActivity(package='com.whatsapp', activity_name='.registration.EULA'): accept_eula,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone'): enter_reg_phone,
    AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber', popup_exists=True, text=TRIED_MANY_TIMES): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='.loginfailure.LogoutMessageActivity'): handle_ban,
    AppActivity(package='com.whatsapp', activity_name='.registration.phonenumberentry.RegisterPhone', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber', popup_exists=True, text="Code verified"): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=CHECK_YOUR_NUMBER): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='.registration.phonenumberentry.RegisterPhone', popup_exists=True, text=IS_CORRECT_NUMBER): handle_is_correct_number,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone', popup_exists=True, text=ENTER_YOUR_NUMBER): enter_reg_phone_or_back,
    AppActivity(package='com.whatsapp', activity_name='.registration.phonenumberentry.RegisterPhone', popup_exists=True, text=ENTER_YOUR_NUMBER): enter_reg_phone_or_back,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone', popup_exists=True, text=OFFER_TO_EDIT_NUMBER): accept_reg_phone,
    AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber', popup_exists=True, text=YOU_TRIED): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=REQUESTING_CODE, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber', popup_exists=True, text=CHECK_YOUR_NUMBER): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='.registration.phonenumberentry.RegisterPhone', popup_exists=True, text=OFFER_TO_EDIT_NUMBER): accept_reg_phone,
    AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber'): enter_reg_code_or_go_back,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone', popup_exists=True, text=PHONE_BANNED): handle_banned_reg_phone,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True,text=SWITCHNG_BUSINESS): handle_switching_business,
    AppActivityWithLikeText(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=NOT_VALID_NUMBER): not_valid,
    AppActivityWithLikeText(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=COULDNT_CALL): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=REQUESTING_CALL, is_loading=True): do_nothing,
    AppActivityWithLikeText(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=YOU_GUESSED): handle_ban_popup_sms,
    AppActivityWithLikeText(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=YOU_HAVE_REQUESTED): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=YOU_TRIED): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone', popup_exists=True, text=UNABLE_CONNECT_PLEASE_CHECK): handle_ban,
    AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone', popup_exists=True, text=SWITCHNG_BUSINESS): handle_switching_business,
    AppActivity(package='com.whatsapp', activity_name='.registration.PrimaryFlashCallEducationScreen'): choose_sms_reg_verify,
    AppActivity(package='com.whatsapp', activity_name='.registration.flashcall.PrimaryFlashCallEducationScreen'): choose_sms_reg_verify,
    AppActivity(package='com.whatsapp', activity_name='.registration.flashcall.PrimaryFlashCallEducationScreen', popup_exists=True, text=VERIFY_NUMBER): choose_sms_reg_verify,
    AppActivity(package='com.whatsapp', activity_name='.registration.flashcall.PrimaryFlashCallEducationScreen', popup_exists=True, text=VERIFY_YOUR_NUMBER): choose_sms_reg_verify,
    AppActivity(package='com.whatsapp', activity_name='.registration.flashcall.PrimaryFlashCallEducationScreen', popup_exists=True, text=VERIFY_NUMBER_ANOTHER_WAY): choose_sms_reg_verify,
    AppActivity(package='com.whatsapp', activity_name='.registration.flashcall.PrimaryFlashCallEducationScreen', popup_exists=True, text=SENDING_CODE, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.verifyphone.VerifyPhoneNumber', popup_exists=True, text=SENDING_CODE, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber'): enter_reg_code_or_go_back,
    AppActivity(package='com.whatsapp', activity_name='.backup.google.GoogleDriveNewUserSetupActivity', popup_exists=True, text='Google storage backup'): never_backup,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=WHATSAPP_UNAVAILABLE): handle_ban_popup_sms,
    AppActivityWithLikeText(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=YOU_RECENTLY_CONNECTED): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=SENDING_CODE, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=CODE_VERIFIED): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=TRIED_MANY_TIMES): handle_ban_popup_sms,
    AppActivity(package='grhmx.b.aplmcqwv', activity_name='s03.V.ay'): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='.RequestPermissionActivity'): accept_permission_request,
    AppActivity(package='com.whatsapp', activity_name='.RequestPermissionActivity', popup_exists=True, text=CONTACTS_AND_MEDIA): handle_go_back,
    AppActivity(package='com.whatsapp', activity_name='.RequestPermissionActivity', popup_exists=True, text=RESTORE_BACKUP): handle_go_back,
    AppActivity(package='com.whatsapp', activity_name='.backup.google.RestoreFromBackupActivity', popup_exists=True, text=BACKUP_PERMISSION): skip_backup,
    AppActivity(package='com.whatsapp', activity_name='.backup.google.RestoreFromBackupActivity', popup_exists=True, text=NEW_BACKUP_PERMISSION): skip_backup,
    AppActivity(package='com.whatsapp', activity_name='.backup.google.RestoreFromBackupActivity', popup_exists=True, text=LOOKING_BACKUPS): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterName'): enter_reg_name,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterName', popup_exists=True, text=UNABLE_CONNECT_TRY_AGAIN): handle_ban,
    AppActivity(package='com.whatsapp', activity_name='.registration.profilecheckpoint.RequestName'): enter_reg_name_spec,
    AppActivity(package='com.whatsapp', activity_name='.registration.profilecheckpoint.RequestName', popup_exists=True, text=SENDING_CODE, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.profilecheckpoint.ProfileCheckpointRegisterName', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.profilecheckpoint.ProfileCheckpointRegisterName'): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone', popup_exists=True, text=SENDING_CODE, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.backup.google.RestoreFromBackupActivity', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterEmail'): handle_register_email,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterEmail', popup_exists=True, text="Enter your email"): handle_register_email_or_back,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterEmail', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text='Unable to connect. Please try again later.'): handle_stop_iteration,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.ContactPicker', popup_exists=True, text='Network unavailable. Please try again later.'): handle_stop_iteration,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone', popup_exists=True, text='WhatsApp is temporarily unavailable. Please try again in 5 minutes.'): handle_stop_iteration,
    AppActivity(package='com.whatsapp', activity_name='.registration.EULA', popup_exists=True, text='Alert'): handle_stop_iteration,
    AppActivity(package='com.whatsapp', activity_name='androidx.credentials.playservices.HiddenActivity'): handle_click_registration_submit,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity'): handle_home,
    # Рассылка через группы
    AppActivity(package='com.whatsapp', activity_name='.community.CommunityNUXActivity'): handle_create_community,
    AppActivity(package='com.whatsapp', activity_name='.community.NewCommunityActivity'): handle_community_settings,
    AppActivity(package='com.whatsapp', activity_name='.community.CommunityNavigationActivity'): handle_add_new_group,
    AppActivity(package='com.whatsapp', activity_name='.community.CommunityNavigationActivity', popup_exists=True, text=ANY): handle_add_new_group_or_back,
    AppActivity(package='com.whatsapp', activity_name='.community.ManageGroupsInCommunityActivity'): handle_create_new_group,
    AppActivity(package='com.whatsapp', activity_name='.group.newgroup.NewGroup'): handle_set_name_group,
    AppActivity(package='com.whatsapp', activity_name='.group.GroupChatInfoActivity'): handle_add_partiсipants,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.AddGroupParticipantsSelector'): handle_choosing_participants,
    AppActivity(package='com.whatsapp', activity_name='.community.AddGroupsToCommunityActivity'): handle_create_new_group,
    AppActivity(package='com.whatsapp', activity_name='.group.GroupPermissionsActivity'): handle_group_permissions,
    AppActivity(package='com.whatsapp', activity_name='.group.GroupMembersSelector'): handle_choosing_participants,
    AppActivity(package='com.whatsapp', activity_name='.community.deactivate.DeactivateCommunityDisclaimerActivity'): handle_deactivate_community,
    AppActivity(package='com.whatsapp', activity_name='.chatinfo.ContactInfoActivity'): handle_contact_info,
    AppActivity(package='com.whatsapp', activity_name='.invites.SMSPreviewInviteGroupParticipantsActivity'): handle_participants_not_now,
    AppActivity(package='com.whatsapp', activity_name='.userban.ui.BanAppealActivity', popup_exists=True, text='Adding...', is_loading=True): handle_ban,
    AppActivity(package='com.whatsapp', activity_name='.settings.SettingsJidNotificationActivity'): handle_go_back,

    #
    AppActivity(package='com.whatsapp', activity_name='.settings.Settings'): handle_settings,
    AppActivity(package='com.whatsapp', activity_name='.profile.ProfileInfoActivity'): handle_profile_settings,
    AppActivity(package='com.whatsapp', activity_name='.gallerypicker.GalleryPicker'): handle_choose_album,
    AppActivity(package='com.whatsapp', activity_name='.gallerypicker.MediaPicker'): handle_choose_photo,
    AppActivity(package='com.whatsapp', activity_name='.gallery.NewMediaPicker'): handle_choose_photo,
    AppActivity(package='com.whatsapp', activity_name='.crop.CropImage'): handle_photo_crop,
    AppActivity(package='com.whatsapp', activity_name='.profile.SetAboutInfo'): handle_about,
    AppActivity(package='com.whatsapp', activity_name='.settings.SettingsAccount'): handle_account_settings,
    AppActivity(package='com.whatsapp', activity_name='.twofactor.SettingsTwoFactorAuthActivity'): handle_twofactor_settings,
    AppActivity(package='com.whatsapp', activity_name='.twofactor.TwoFactorAuthActivity'): handle_twofactor_settings_inner,
    AppActivity(package='com.whatsapp', activity_name='.ContactPicker', popup_exists=True, text=NOT_VALID): handle_not_valid,
    AppActivity(package='com.whatsapp', activity_name='.ContactPicker', popup_exists=True, text=COULDNT_FIND_PHONE): handle_couldnt_find_phone,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.ContactPicker', popup_exists=True, text=NOT_VALID): handle_not_valid,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.ContactPicker', popup_exists=True, text=COULDNT_FIND_PHONE): handle_couldnt_find_phone,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text=NOT_VALID): handle_not_valid,
    AppActivity(package='com.whatsapp', activity_name='.TextAndDirectChatDeepLink', popup_exists=True, text=NOT_VALID): handle_not_valid,
    AppActivity(package='com.whatsapp', activity_name='.Conversation'): handle_conversation,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text=DELETE_CHAT): handle_delete_chat,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text=DELETE_CHAT2): handle_delete_chat,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text=DELETE_CHAT3): handle_delete_chat,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text=PLEASE_WAIT, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text='Chats'): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.backup.google.GoogleDriveNewUserSetupActivity'): handle_google_drive,
    AppActivity(package='com.whatsapp', activity_name='.backup.google.GoogleDriveNewUserSetupActivity', popup_exists=True, text="Google Drive backup"): handle_google_drive_or_back,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=START_CALL): accept_call_start,
    AppActivity(package='com.whatsapp', activity_name='.calling.spam.CallSpamActivity'): handle_spam_call,
    AppActivity(package='com.whatsapp', activity_name='.mediacomposer.MediaComposerActivity'): handle_send_attachments,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=NEW_WEB): handle_new_web,
    AppActivity(package='com.whatsapp', activity_name='.companiondevice.LinkedDevicesActivity'): handle_linked_devices,
    AppActivity(package='com.whatsapp', activity_name='.companiondevice.LinkedDevicesActivity', popup_exists=True, text=CONNECT_WIFI): handle_connect_wifi,
    AppActivity(package='com.whatsapp', activity_name='.qrcode.DevicePairQrScannerActivity'): handle_pair_web,
    AppActivity(package='com.whatsapp', activity_name='.qrcode.DevicePairQrScannerActivity', popup_exists=True, text=CHECK_INTERNET): handle_web_check_internet,
    AppActivity(package='com.whatsapp', activity_name='.companiondevice.LinkedDevicesActivity', popup_exists=True, text=ANY): handle_web_logout,
    AppActivity(package='com.whatsapp', activity_name='.qrcode.DevicePairQrScannerActivity', popup_exists=True, text=COULDNT_LINK): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.qrcode.DevicePairQrScannerActivity', popup_exists=True, text=LOGGING_IN, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.profile.SetAboutInfo', is_loading=True): do_nothing,
    AppActivity(package='com.samsung.android.app.contacts', activity_name='com.samsung.android.contacts.contactslist.PeopleActivity'): handle_samsung_contacts,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyCaptcha'): handle_captcha,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyCaptcha', popup_exists=True, text=MANY_ATTEMPTS): handle_captcha,
    # AppActivity(package='com.whatsapp', activity_name='.calling.VoipNotAllowedActivity'): do_nothing, #TODO разобраться что такое
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=IS_CORRECT_NUMBER): handle_is_correct_number,
    AppActivity(package='com.joeykrim.rootcheck', activity_name='.MainActivity'): handle_is_correct_number,
    AppActivity(package='g.y.f.q', activity_name='e.dk.D'): handle_is_correct_number,
    # AppActivity(package='com.whatsapp', activity_name='.Conversation', popup_exists=True, text=SURE_INTERNET_CONNECTION): handle_popup_ok,
    # AppActivity(package='com.whatsapp', activity_name='.Conversation', popup_exists=True, text=PLACE_WHATSAPP_CALL): handle_conversation_airmode,
    # AppActivity(package='com.whatsapp', activity_name='.Conversation', popup_exists=True, text=DOCUMENT): handle_attachments,
    # AppActivityWithLikeText(package='com.whatsapp', activity_name='.Conversation', popup_exists=True, text=JUST_ANSWERED_CALL): handle_decline,
    # AppActivity(package='com.whatsapp', activity_name='.Conversation', popup_exists=True, text=DOCUMENT): handle_group_image_sending,

    AppActivity(package='com.whatsapp', activity_name='.Conversation', popup_exists=True, text=ANY): handle_conversation_popup,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.ContactPicker', popup_exists=True, text="Select contact"): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text="Select contact"): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.community.CommunityNUXActivity', popup_exists=True, text="Create a new community"): handle_create_community_or_nothing,
    AppActivity(package='com.whatsapp', activity_name='.community.NewCommunityActivity', popup_exists=True, text="New community"): handle_set_text_or_nothing,
    AppActivity(package='com.whatsapp', activity_name='.Main', popup_exists=True, text="WhatsApp"): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text="WhatsApp"): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyTwoFactorAuth'): handle_go_back,
    AppActivity(package='com.whatsapp', activity_name='.Main', popup_exists=True, text='Initializing...', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterName', popup_exists=True, text='Initializing...', is_loading=True): do_nothing,
    AppActivity(package='tw.i.rewrufthlf.rfj', activity_name=ANY): do_nothing,
    AppActivity(package='ceeyvrrgau.e', activity_name=ANY): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.HomeActivity', popup_exists=True, text='Invite your friends'): handle_stop_iteration,
    AppActivity(package='com.whatsapp', activity_name='.registration.email.EmailEducationScreen'): skip_email,

    # СЛУЧАЙНЫЕ ОКНА WHATSAPP
    AppActivity(package='com.whatsapp', activity_name='.userban.ui.BanAppealActivity'): handle_ban,
    AppActivity(package='com.whatsapp', activity_name='.userban.ui.BanAppealActivity', popup_exists=True, text=ANY): handle_ban,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=PHONE_NO_LONGER_REG): handle_ban,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=ENTER_PIN): enter_pin,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=NEW): skip_new,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=NEW2): skip_new,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=CODE_REQUESTED): handle_smb_requested_code,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=VERIFY_YOUR_ACCOUNT): handle_ban,
    AppActivity(package='com.whatsapp', activity_name='.registration.parole.CustomRegistrationBlockActivity'): handle_ban,

    # БЫСТРЫЕ ОКНА WHATSAPP
    AppActivity(package='com.whatsapp', activity_name='.voipcalling.VoipPermissionsActivity'): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.voipcalling.VoipActivityV2'): handle_voip_activity,
    AppActivity(package='com.whatsapp', activity_name='.voipcalling.VoipActivityV2', is_call=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.TextAndDirectChatDeepLink'): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.backup.google.RestoreFromBackupActivity'): handle_loading_backup,
    AppActivity(package='com.whatsapp', activity_name='.Main'): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.ContactPicker'): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.ContactPicker'): handle_contacts,
    AppActivity(package='com.whatsapp', activity_name='com.android.internal.app.ResolverActivity'): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterPhone', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.calling.callrating.CallRatingActivityV2'): handle_call_rating,
    AppActivity(package='com.whatsapp', activity_name='.registration.VerifyPhoneNumber', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.AddGroupParticipantsSelector', is_loading=True): handle_participants_add,
    AppActivity(package='com.whatsapp', activity_name='.group.GroupChatInfoActivity', is_loading=True): handle_special_participants,
    AppActivity(package='com.whatsapp', activity_name='.group.GroupChatInfoActivity', popup_exists=True, text=PARTICIPANT_CANNOT_BE_ADDED): handle_participants_cant_added,
    AppActivity(package='com.whatsapp', activity_name='.group.GroupChatInfoActivity', popup_exists=True, text=ANY): handle_participants_cant_added_phones,
    AppActivity(package='com.whatsapp', activity_name='.community.NewCommunityActivity', popup_exists=True, text="Creating community...", is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.community.NewCommunityActivity', popup_exists=True, text=INVALID_PHOTO_RESOLUTION): handle_bad_resolution,
    AppActivity(package='com.whatsapp', activity_name='.group.newgroup.NewGroup', popup_exists=True, text=INVALID_PHOTO_RESOLUTION): handle_bad_resolution,
    AppActivity(package='com.whatsapp', activity_name='.group.newgroup.NewGroup', popup_exists=True, text="Creating group", is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.community.AddGroupsToCommunityActivity', popup_exists=True, text="Creating community...", is_loading=True): do_nothing,
    AppActivityWithLikeText(package='com.whatsapp', activity_name='.contact.picker.AddGroupParticipantsSelector', popup_exists=True, text=ANY): handle_participants_community_add,
    AppActivity(package='com.whatsapp', activity_name='.community.CommunityHomeActivity'): handle_participants_cant_added,
    AppActivity(package='com.whatsapp', activity_name='.community.CommunityHomeActivity', popup_exists=True, text=ANY): handle_community_home_popups,
    AppActivity(package='com.whatsapp', activity_name='.community.deactivate.DeactivateCommunityDisclaimerActivity', popup_exists=True, text=ANY): handle_deactivate_community_popup,
    AppActivity(package='com.whatsapp', activity_name='.community.deactivate.DeactivateCommunityDisclaimerActivity', popup_exists=True, text="Deactivating community...", is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.community.CommunityHomeActivity', popup_exists=True, text="Adding...", is_loading=True): do_nothing,
    # AppActivity(package='com.whatsapp', activity_name='.community.CommunityHomeActivity', popup_exists=True, text=PARTICIPANT_CANNOT_BE_ADDED): handle_ban,
    AppActivity(package='com.whatsapp', activity_name='.invites.InviteGroupParticipantsActivity'): handle_community_home_popups,

    # ЗАГРУЗКИ / УСПЕШНЫЕ ЗАГРУЗКИ WHATSAPP
    AppActivity(package='com.whatsapp', activity_name='.ContactPicker', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.RequestPermissionActivity', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.RegisterName', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=CONNECTING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=REQUESTING_AN_SMS, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=REQUESTING_AN_SMS_INSTEAD, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=VERIFYING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=VERIFICATION_COMPLETE): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=LOADING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=APPLYING_SETTINGS, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=SEARCHING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name=ANY, popup_exists=True, text=UPDATING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.group.GroupChatInfoActivity', popup_exists=True, text="Adding...", is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.AddGroupParticipantsSelector', popup_exists=True, text="Adding...", is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.gallerypicker.GalleryPickerBottomSheetActivity'): handle_group_image_choose,
    AppActivity(package='com.whatsapp', activity_name='.registration.email.EmailEducationScreen', popup_exists=True, text='Initializing...', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.registration.email.EmailEducationScreen', is_loading=True): do_nothing,

    # ОКНА WHATSAPP BUSINESS
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.EULA'): accept_eula,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterPhone'): enter_reg_phone,
    AppActivityWithLikeText(package='com.whatsapp.w4b', activity_name='.registration.RegisterPhone', popup_exists=True, text=NOT_VALID_NUMBER): not_valid,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterPhone', popup_exists=True, text=OFFER_TO_EDIT_NUMBER): accept_reg_phone,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterPhone', popup_exists=True, text=PHONE_BANNED): handle_banned_reg_phone,
    AppActivityWithLikeText(package='com.whatsapp', activity_name='.registration.phonenumberentry.RegisterPhone', popup_exists=True, text=SWITCHNG_BUSINESS_PATTERN): handle_switching_business,
    AppActivityWithLikeText(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.VerifyPhoneNumber', popup_exists=True, text=COULDNT_CALL): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp', activity_name='com.whatsapp.registration.VerifyPhoneNumber', popup_exists=True, text=REQUESTING_CALL, is_loading=True): do_nothing,
    AppActivityWithLikeText(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.VerifyPhoneNumber', popup_exists=True, text=YOU_GUESSED): handle_ban_popup_sms,
    AppActivityWithLikeText(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.VerifyPhoneNumber', popup_exists=True, text=YOU_HAVE_REQUESTED): handle_ban_popup_sms,
    # AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterPhone', popup_exists=True, text=UNABLE_CONNECT_PLEASE_CHECK): handle_ban,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterPhone', popup_exists=True, text=SWITCHNG_BUSINESS): handle_switching_business,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterPhone', popup_exists=True, text=SWITCHNG_BUSINESS2): handle_switching_business,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.PrimaryFlashCallEducationScreen'): choose_sms_reg_verify,
    AppActivity(package='com.whatsapp.w4b', activity_name='.registration.flashcall.PrimaryFlashCallEducationScreen'): choose_sms_reg_verify,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.VerifyPhoneNumber'): enter_reg_code_or_go_back,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.VerifyPhoneNumber', popup_exists=True, text=CHECK_YOUR_NUMBER): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.VerifyPhoneNumber', popup_exists=True, text=WHATSAPP_UNAVAILABLE): handle_ban_popup_sms,
    AppActivityWithLikeText(package='com.whatsapp.w4b', activity_name='.registration.VerifyPhoneNumber', popup_exists=True, text=YOU_RECENTLY_CONNECTED): handle_ban_popup_sms,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.RequestPermissionActivity'): accept_permission_request,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.backup.google.RestoreFromBackupActivity', popup_exists=True, text=BACKUP_PERMISSION): skip_backup,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterName'): enter_reg_name,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterName', popup_exists=True, text=UNABLE_CONNECT_TRY_AGAIN): handle_ban,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.businessprofilecategory.EditBusinessCategoryActivity'): handle_category,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.HomeActivity'): handle_home,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.settings.Settings'): handle_settings,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.profile.ProfileInfoActivity'): handle_profile_settings,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.businessprofileedit.EditBusinessProfileActivity'): handle_profile_settings_b,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.gallerypicker.GalleryPicker'): handle_choose_album,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.gallerypicker.MediaPicker'): handle_choose_photo,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.gallery.NewMediaPicker'): handle_choose_photo,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.crop.CropImage'): handle_photo_crop,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.profile.SetAboutInfo'): handle_about,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.settings.SettingsAccount'): handle_account_settings,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.twofactor.SettingsTwoFactorAuthActivity'): handle_twofactor_settings,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.twofactor.TwoFactorAuthActivity'): handle_twofactor_settings_inner,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.ContactPicker', popup_exists=True, text=NOT_VALID): handle_not_valid,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.ContactPicker', popup_exists=True, text=COULDNT_FIND_PHONE): handle_couldnt_find_phone,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.contact.picker.ContactPicker', popup_exists=True, text=NOT_VALID): handle_not_valid,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.contact.picker.ContactPicker', popup_exists=True, text=COULDNT_FIND_PHONE): handle_couldnt_find_phone,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.HomeActivity', popup_exists=True, text=NOT_VALID): handle_not_valid,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.TextAndDirectChatDeepLink', popup_exists=True, text=NOT_VALID): handle_not_valid,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.Conversation'): handle_conversation,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.HomeActivity', popup_exists=True, text=DELETE_CHAT): handle_delete_chat,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.HomeActivity', popup_exists=True, text=DELETE_CHAT2): handle_delete_chat,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.HomeActivity', popup_exists=True, text=DELETE_CHAT3): handle_delete_chat,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.HomeActivity', popup_exists=True, text=PLEASE_WAIT, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.backup.google.GoogleDriveNewUserSetupActivity'): handle_google_drive,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.Conversation', popup_exists=True, text=START_CALL): accept_call_start,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.Conversation', popup_exists=True, text=DOCUMENT): handle_attachments,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.mediacomposer.MediaComposerActivity'): handle_send_attachments,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=NEW_WEB): handle_new_web,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.companiondevice.LinkedDevicesActivity'): handle_linked_devices,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.companiondevice.LinkedDevicesActivity', popup_exists=True, text=CONNECT_WIFI): handle_connect_wifi,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.qrcode.DevicePairQrScannerActivity'): handle_pair_web,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.qrcode.DevicePairQrScannerActivity', popup_exists=True, text=CHECK_INTERNET): handle_web_check_internet,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.companiondevice.LinkedDevicesActivity', popup_exists=True, text=ANY): handle_web_logout,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.qrcode.DevicePairQrScannerActivity', popup_exists=True, text=COULDNT_LINK): handle_couldnt_link,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.qrcode.DevicePairQrScannerActivity', popup_exists=True, text=LOGGING_IN, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.profile.SetAboutInfo', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.businessregistration.OnboardingActivity'): skip_onboarding,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.businessregistration.ChangeBusinessNameActivity'): handle_edit_name,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.smbmultideviceagents.view.activity.BizAgentDevicesActivity'): handle_linked_devices,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.smbmultideviceagents.view.activity.BizAgentDevicesActivity', popup_exists=True, text=CONNECT_WIFI): handle_connect_wifi,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.smbmultideviceagents.view.activity.SetDeviceNameActivity'): handle_set_name_b,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.gallerypicker.GalleryPickerLauncher'): handle_choose_album,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.contact.picker.ContactPicker'): handle_contacts,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.profile.ViewProfilePhoto'): handle_viewer_photo,

    # СЛУЧАЙНЫЕ ОКНА WHATSAPP BUSINESS
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.userban.ui.BanAppealActivity'): handle_ban,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=PHONE_NO_LONGER_REG): handle_ban,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=ENTER_PIN): enter_pin,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=NEW): skip_new,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=NEW2): skip_new,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=LINK_FB): handle_link_fb,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=CODE_REQUESTED): handle_smb_requested_code,

    # БЫСТРЫЕ ОКНА WHATSAPP BUSINESS
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.voipcalling.VoipPermissionsActivity'): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.voipcalling.VoipActivityV2'): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.TextAndDirectChatDeepLink'): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.backup.google.RestoreFromBackupActivity'): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.Main'): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.ContactPicker'): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.android.internal.app.ResolverActivity'): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.smbmultideviceagents.view.activity.AgentDeviceInfoActivity'): do_nothing,

    # ЗАГРУЗКИ / УСПЕШНЫЕ ЗАГРУЗКИ WHATSAPP BUSINESS
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.ContactPicker', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.RequestPermissionActivity', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name='com.whatsapp.registration.RegisterName', is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=CONNECTING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=REQUESTING_AN_SMS, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=VERIFYING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=VERIFICATION_COMPLETE): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=LOADING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=APPLYING_SETTINGS, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=SEARCHING, is_loading=True): do_nothing,
    AppActivity(package='com.whatsapp.w4b', activity_name=ANY, popup_exists=True, text=UPDATING, is_loading=True): do_nothing,

    # ЗАКРЫВАЮЩИЕ ДЛЯ ОКОН СИСТЕМЫ
    AppActivity(package='com.sec.android.app.launcher', activity_name=ANY, popup_exists=ANY, text=ANY, is_loading=ANY): do_nothing,
    AppActivity(package='com.google.android.permissioncontroller', activity_name=ANY): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.gallerypicker.GalleryPickerLauncher'): do_nothing,
    AppActivity(package=ANY, activity_name='.activities.LauncherActivity'): do_nothing,
    AppActivity(package=ANY, activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity'): allow_permission,
    # AppActivity(package=ANY, activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity'): do_nothing,
    AppActivity(package=ANY, activity_name='.ui.surequest.SuRequestActivity'): do_nothing,
    AppActivity(package='com.sec.android.app.launcher', activity_name='com.whatsapp.businessprofileedit.EditBusinessProfileActivity'): handle_choose_album,
    AppActivity(package=ANY, activity_name='d.b'): do_nothing,
    AppActivity(package='com.wssyncmldm', activity_name='com.idm.fotaagent.enabler.ui.downloadconfirm.DownloadConfirmActivity'): click_home, #do_nothing,


    # ПРОКСИ
    AppActivity(package='org.sandroproxy.drony', activity_name='.DronyMainActivity'): handle_drony,
    AppActivity(package='com.google.android.permissioncontroller', activity_name='com.android.permissioncontroller.permission.ui.GrantPermissionsActivity', popup_exists=True, text=ALLOW_DRONY): handle_drony_permission,
    AppActivity(package='com.android.vpndialogs', activity_name='.ConfirmDialog', popup_exists=True, text='Connection request'): handle_drony_icon,
    AppActivity(package='com.android.vpndialogs', activity_name='.ConfirmDialog'): do_nothing,
    AppActivity(package='com.whatsapp', activity_name='.contact.picker.ContactPicker', popup_exists=True, text='Please try again later.'): handle_try_again,
})
