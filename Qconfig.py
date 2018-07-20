# Before you can use the jobs API, you need to set up an access token.
# Log in to the Quantum Experience. Under "Account", generate a personal 
# access token. Replace "None" below with the quoted token string.
# Uncomment the APItoken variable, and you will be ready to go.

APItoken = "1e46a0b67a7237c5da1093d2fe96af1c35f40dae53706c0f67330e31613c9a482a1c85cc33942780bd3d4fa42c968271628b5782e98499d381d634aa5d4e69ec"


config = {
  "url": 'https://quantumexperience.ng.bluemix.net/api'
}

if 'APItoken' not in locals():
  raise Exception("Please set up your access token. See Qconfig.py.")
