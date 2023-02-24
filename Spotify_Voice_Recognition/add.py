from flask import Flask, request, redirect
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
import speech_recognition as sr
import json

app = Flask(__name__)

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'http://localhost:3000/callback' # your redirect URI
CLIENT_ID = "0b641ee8238d4e6186fc57a4b5c5bef5"
CLIENT_SECRET = "4f6d0a885480435b829592422ff85c47"
SCOPE = [
    "user-read-playback-state",
    "app-remote-control",
    "user-modify-playback-state",
    "playlist-read-private",
    "playlist-read-collaborative",
    "user-read-currently-playing",
    "user-read-playback-position",
    "user-library-modify",
    "playlist-modify-private",
    "playlist-modify-public",
    "user-read-recently-played",
    "user-read-private",
    "user-library-read"
]
def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def get_headers(token):
    return {"Authorization": "Bearer " + token}

@app.route("/login")
def login():
    spotify = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = spotify.authorization_url(AUTH_URL)
    return redirect(authorization_url)

# your redirect URI's path
@app.route("/callback", methods=['GET'])
def callback():
    code = request.args.get('code')
    res = requests.post(TOKEN_URL,
                        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
                        data={
                            'grant_type': 'authorization_code',
                            'code': code,
                            'redirect_uri': REDIRECT_URI
                        })
    access_token = res.json()['access_token']
    listObj = []
    listObj.append(res.json())

    # get current playing
    headers = get_headers(access_token)
    result1 = requests.get(url='https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    current_song = result1.json()
    listObj.append(current_song)

    # Add new song into playlist with current playing song
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=1)

    while True:
        print("Say something!")
        speech = recognize_speech_from_mic(recognizer, microphone)
        print(speech)
        if speech["error"]:
            print("ERROR: {}".format(speech["error"]))
        else:
            command = speech["transcription"].lower()
            playlist=""
            match command:
                case "one":
                    playlist="4cJfwDqigQl0gOQhQfLkj7"
                case "technology":
                    playlist="2rolbhUAQ5Dkxn5BQrmEui"
                case "romeo":
                    playlist="7gGawef6WzQQ1wVB3Dn4vg"

            url = "https://api.spotify.com/v1/playlists/{0}/tracks".format(playlist)
            # current_song['item']['uri']  = 'spotify:track:xxxxxxxxxxxxxxxx'
            params = {'uris': current_song['item']['uri']}
            result2 = requests.post(url,
                            params=params,
                            headers={'Content-Type':'application/json',
                                     'Authorization': 'Bearer {0}'.format(access_token)})
            added_song = result2.json()
            listObj.append(added_song)
    return listObj

if __name__ == '__main__':

    app.run(port=3000,debug=True) # your redirect URI's port