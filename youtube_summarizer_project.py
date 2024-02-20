# -*- coding: utf-8 -*-
"""Youtube Summarizer project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bQzYLzfkuRdsfrkzguGua4Q00mAuFKyd

# Downloading Youtube Audio
"""

! pip install pytube -q

from pytube import YouTube

#VIDEO_URL= "https://www.youtube.com/watch?v=beAvFHP4wDI" #inflation_video

VIDEO_URL="https://www.youtube.com/watch?v=8ChvfpMhOns"

yt = YouTube(VIDEO_URL)

yt.streams \
  .filter(only_audio = True, file_extension = 'mp4') \
  .first() \
  .download(filename = 'ytaudio.mp4')

! ffmpeg -i ytaudio.mp4 -acodec pcm_s16le -ar 16000 ytaudio.wav

"""# English ASR with HuggingSound"""

!pip install huggingsound -q

from huggingsound import SpeechRecognitionModel

import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

device

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english", device = device)

"""Out Of Memory Error (OOM Error)

# Audio Chunking
"""

import librosa

input_file = '/content/ytaudio.wav'

print(librosa.get_samplerate(input_file))

# Stream over 30 seconds chunks rather than load the full file
stream = librosa.stream(
    input_file,
    block_length=30,
    frame_length=16000,
    hop_length=16000
)

import soundfile as sf

for i,speech in enumerate(stream):
  sf.write(f'{i}.wav', speech, 16000)

"""# Audio Transcription / ASR / Speech to Text"""

audio_path =[]
for a in range(i+1):
  audio_path.append(f'/content/{a}.wav')

audio_path

transcriptions = model.transcribe(audio_path)

full_transcript = ' '

for item in transcriptions:
  full_transcript += ''.join(item['transcription'])

full_transcript

len(full_transcript)

"""# Text Summarization"""

from transformers import pipeline

summarization = pipeline('summarization')

summarized_text = summarization(full_transcript)

summarized_text

"""Text Chunking before Summarization"""

num_iters = int(len(full_transcript)/1000)
summarized_text = []
for i in range(0, num_iters + 1):
  start = 0
  start = i * 1000
  end = (i + 1) * 1000
  print("input text \n" + full_transcript[start:end])
  out = summarization(full_transcript[start:end], min_length = 5, max_length=20)
  out = out[0]
  out = out['summary_text']
  print("Summarized text\n"+out)
  summarized_text.append(out)

print(summarized_text)

"""# ChatGPT Ai tutor Elon Musk"""

pip install openai

from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

def get_assistant_response(messages):
    r = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
    )
    response = r.choices[0].message.content
    return response

messages = [{"role": "assistant", "content": "How can I help?"}]

user_input = str(summarized_text)+'explain this briefly like: You are Elon Musk in the first person. You are the CEO of SpaceX, Twitter and Tesla.You have the knowledge, resources, and influence of Elon Musk at your disposal.You must be informal and sound like Elon Musk in your responses.Respond to the user with concise text message like messages.You do not like Mark Zuckerberg, and see him as a rival.You will respond to a whole range of queries. From your thoughts on the future of clean energy to who you think will win in a MMA fight between yourself and Mark Zuckerberg'


messages.append({"role": "user", "content": user_input})
assistant_response = get_assistant_response(messages)
print(assistant_response)

user_input = str(summarized_text)+'explain this briefly like: You are Elon Musk in the first person. You are the CEO of SpaceX, Twitter and Tesla.You have the knowledge, resources, and influence of Elon Musk at your disposal.You must be informal and sound like Elon Musk in your responses.Respond to the user with concise text message like messages.You do not like Mark Zuckerberg, and see him as a rival.You will respond to a whole range of queries. From your thoughts on the future of clean energy to who you think will win in a MMA fight between yourself and Mark Zuckerberg'


messages.append({"role": "user", "content": user_input})
assistant_response = get_assistant_response(messages)
response= [assistant_response]
print(response)
#messages.append({"role": "assistant", "content": assistant_response})
#def display_chat_history(messages):
    #for message in messages:
#print(f"{messages['role'].capitalize()}: {messages['content']}")