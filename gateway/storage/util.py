import pika, json

def upload(f, fs, channel, access):
    try:
        fid =fs.put(f)
    except Exception as e:
        return 'File upload failed', 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access['username']
    }

    try:
        channel.basic_publish(
            exchange='', 
            routing_key='video', 
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,  # make message persistent
            )
        )
    except Exception as e:
        fs.delete(fid)
        return 'File upload failed', 500