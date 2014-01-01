# this example is a snippet from an NFC p2p app, and are located into a
# kivy App class implementation

from android import activity

def on_new_intent(self, intent):
    if intent.getAction() != NfcAdapter.ACTION_NDEF_DISCOVERED:
        return
    rawmsgs = intent.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES)
    if not rawmsgs:
        return
    for message in rawmsgs:
        message = cast(NdefMessage, message)
        payload = message.getRecords()[0].getPayload()
        print 'payload: {}'.format(''.join(map(chr, payload)))

def nfc_enable(self):
    activity.bind(on_new_intent=self.on_new_intent)
    # ...

def nfc_disable(self):
    activity.unbind(on_new_intent=self.on_new_intent)
    # ...