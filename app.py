import os
import web
import random
import SimpleCV

urls = (".*","index")
PROJECT_DIR = os.path.dirname(__file__)
render = web.template.render(os.path.join(PROJECT_DIR, 'templates'))

def randstr(length=10):
        return "".join([chr(random.randrange(97,123)) for i in range(length)])

def glassface(image, save_new = True):
        face_cascade = SimpleCV.HaarCascade("/usr/local/lib/python2.7/dist-packages/SimpleCV/Features/HaarCascades/face.xml")
        glasses = SimpleCV.Image("/usr/local/lib/python2.7/dist-packages/SimpleCV/sampleimages/deal_with_it.png")
        mask = SimpleCV.Image("deal_with_it_mask.png")
        result_faces = []
        faces = image.findHaarFeatures(face_cascade)
        if faces:
                for face in faces:
                        scale = (face.width() * 1.2)/float(glasses.width)
                        scaled_glasses = glasses.scale(scale)
                        scaled_mask = mask.scale(scale)
                        new_pos = (
                                face.x - scaled_glasses.width/2-face.width()/6, 
                                face.y-scaled_glasses.height/2-face.height()/8
                                )
                        image = image.blit(scaled_glasses, pos = new_pos, mask=scaled_mask)
                        image.save(os.path.join(PROJECT_DIR, "static","%s.jpg" % randstr()))
        return (image.filename.replace(PROJECT_DIR, ""), faces)

class index:
	def GET(self):
		data = web.input()
		new_image = None
		url = data.get('url')
                message = None
                faces = None
		if url:
                        try:
                                new_image, faces = glassface(SimpleCV.Image(url), save_new=False)
                        except Exception, e:
                                message = str(e)
		return render.index(new_image, url, faces, message)


application = web.application(urls, globals())
if __name__ == "__main__": application.run()

