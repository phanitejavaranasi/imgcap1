from flask import Flask,render_template,request


app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=1
def captions(x):
    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
    from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
    from msrest.authentication import CognitiveServicesCredentials


    subscription_key = "12ee0799d65941c98764fa7a1daae4ed"
    endpoint = "https://imagecaption123.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))



    local_image_path=x
    local_image = open(local_image_path, "rb")

    # Call API
    description_result = computervision_client.describe_image_in_stream(local_image)

    # Get the captions (descriptions) from the response, with confidence level
    print("Description of local image: ")
    if (len(description_result.captions) == 0):
        print("No description detected.")
    else:
        for caption in description_result.captions:
            print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
    print()
    return caption.text


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def capture():
    return render_template('Capture.png')

@app.route('/after', methods=['GET', 'POST'])
def after():
    
    
    img = request.files['file1']

    img.save('static/file.jpg')
    
   
    x="static/file.jpg"
    final=captions(x)
    
    
    return render_template('predict.html',final=final)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True,threaded=False)
