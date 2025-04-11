import pika, json, tempfile, os
from bson.objectid import ObjectId
from moviepy import *

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    tf =    tempfile.NamedTemporaryFile()
    out = fs_videos.get(ObjectId(message['video_fid']))
    tf.write(out.read())
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    f = open(tf_path,"rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)

    message['mp3_fid'] = str(fid)

    try:
        channel.basic_publish(
            exchange='', 
            routing_key=os.environ.get('MP3_QUEUE'), 
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,  # make message persistent
            )
        )
    except Exception as e:
        fs_mp3s.delete(fid)
        return "File upload failed and to publish message"
