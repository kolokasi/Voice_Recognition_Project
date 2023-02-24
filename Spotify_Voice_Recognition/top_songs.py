import speech_recognition as sr
import subprocess
from requests import post,put,get
import base64
import json


client_id="0b641ee8238d4e6186fc57a4b5c5bef5"
client_secret="4f6d0a885480435b829592422ff85c47"
auth_token="BQBEG6ctrNHagTlw2BLeRknse0H3B2Sr-Xwy5YsF1XplMHwxwAIdFoyoJRjUdlvsr9TmKJONEHHa5k6b65gp1PDPV9cOYrW9VaekMCIb0apTMSM9AyWu"

def get_token():
    auth_str = client_id + ":" + client_secret
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()
headers =  {"Authorization": "Bearer " + token}
def get_headers(token):
    return {"Authorization": "Bearer " + token}

def search_for_artists(token, artists_name):
    url="https://api.spotify.com/v1/search"
    headers = get_headers(token)
    query = f"?q={artists_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No aritsts exists with that name...")
        return none
    return json_result[0]

def get_song(token, artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

artist = search_for_artists(token, "ACDC")
artist_id = artist["id"]
songs = get_song(token, artist_id)
for i, song in enumerate(songs):
    print(f"{i+1}. {song['name']}")

#NEEDS FIXING, GETTING 404 AS RESPONSE
def get_current_track_and_post_in_playlist(token):
    headers = get_headers(token)
    result = get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    playlist_id = "0p4d0akcszc87kcf0pym6qws1"
    print(result)
    #json_result = json.loads(result.content)["item"]["uri"]
    #print(json_result)

    #playlist_put = post(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={json_result}', headers=headers)


    return True

a = get_current_track_and_post_in_playlist(token)

# def recognize_speech_from_mic(recognizer, microphone):
#     """Transcribe speech from recorded from `microphone`.
#
#     Returns a dictionary with three keys:
#     "success": a boolean indicating whether or not the API request was
#                successful
#     "error":   `None` if no error occured, otherwise a string containing
#                an error message if the API could not be reached or
#                speech was unrecognizable
#     "transcription": `None` if speech could not be transcribed,
#                otherwise a string containing the transcribed text
#     """
#     # check that recognizer and microphone arguments are appropriate type
#     if not isinstance(recognizer, sr.Recognizer):
#         raise TypeError("`recognizer` must be `Recognizer` instance")
#
#     if not isinstance(microphone, sr.Microphone):
#         raise TypeError("`microphone` must be `Microphone` instance")
#
#     # adjust the recognizer sensitivity to ambient noise and record audio
#     # from the microphone
#     with microphone as source:
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#
#     # set up the response object
#     response = {
#         "success": True,
#         "error": None,
#         "transcription": None
#     }
#
#     # try recognizing the speech in the recording
#     # if a RequestError or UnknownValueError exception is caught,
#     #     update the response object accordingly
#     try:
#         response["transcription"] = recognizer.recognize_google(audio)
#     except sr.RequestError:
#         # API was unreachable or unresponsive
#         response["success"] = False
#         response["error"] = "API unavailable"
#     except sr.UnknownValueError:
#         # speech was unintelligible
#         response["error"] = "Unable to recognize speech"
#
#     return response
#
# if __name__ == "__main__":
#     # set up the recognizer and microphone
#     recognizer = sr.Recognizer()
#     microphone = sr.Microphone(device_index=1)
#
#     while True:
#         print("Say something!")
#         speech = recognize_speech_from_mic(recognizer, microphone)
#         print(speech)
#         if speech["error"]:
#             print("ERROR: {}".format(speech["error"]))
#         else:
#             command = speech["transcription"].lower()
#             artist = search_for_artists(token, command)
#             artist_id = artist["id"]
#             songs = get_song(token, artist_id)
#             for i, song in enumerate(songs):
#                 print(f"{i+1}. {song['name']}")
