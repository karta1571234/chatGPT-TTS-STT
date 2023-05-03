import azure.cognitiveservices.speech as speechsdk
import os
import openai


def stt():
    # Azure STT API key
    speech_key, service_region = "<your api key>", "eastus"
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region, speech_recognition_language='zh-TW')
    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Say something...")

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("語音辨識結果: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("沒有匹配的語音: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(
                cancellation_details.error_details))
    return result


def gpt(input):
    # ChatGPT API key
    openai.api_key = f'<your api key>'

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
              {"role": "system", "content": "系統訊息，目前無用"},
              {"role": "assistant", "content": "此處填入機器人訊息"},
              {"role": "user", "content": input}
        ]
    )

    response = completion.choices[0].message.content
    print(f"ChatGPT回應:{response}")
    return response


def tts(input):
    # Azure TTS API key
    speech_key, service_region = "<your api key>", "eastus"
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region, speech_recognition_language='zh-TW')
    # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
    speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"
    # Creates a synthesizer with the given settings
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config)

    # Synthesizes the received text to speech.
    result = speech_synthesizer.speak_text_async(input).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(input))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(
                    cancellation_details.error_details))
        print("Did you update the subscription info?")


if __name__ == "__main__":
    tts("你好~有什麼我可以幫你的嗎? 如果想結束對話可以說:離開或掰掰")
    
    while True:
        result_stt = stt().text
        # result_stt = "我想測試"
        if(result_stt == ""):
            # 語音辨識失敗
            print("語音辨識失敗")
            tts("語音辨識失敗，請再說一次")
        elif(result_stt == "離開。" or result_stt == "掰掰。" or result_stt == "byebye。" or result_stt == "白白。"):
            result_gpt = gpt(result_stt)
            tts(result_gpt)
            print("結束對話")
            break;
        else:
            # 語音辨識成功
            result_gpt = gpt(result_stt)
            tts(result_gpt)
        