'''
Turbo Meme Generator
	Requirements
		Python 3.4(.2)
		Pillow (fork of PIL)
'''

#Prints error and exits with code 1
#Returns nothing
def error(str):
	print("ERROR!: " + str)
	exit(1)

#Importing
try:
	import argparse
except ImportError:
	error("argparse cannot be imported")
	
try:
	import configparser
except ImportError:
	error("argparse cannot be imported")
	
try:
	import os
except ImportError:
	error("os cannot be imported")
	
try:
	import random
except ImportError:
	error("random cannot be imported")
	
try:
	from PIL import Image, ImageOps
except ImportError:
	error("Image from PIL cannot be imported")
	
defaultConfig = {
	"templates": "./database/templates",
	"simages" : "./database/simages",
	"unused" : "./database/unused.txt",
	"image-quality" : 50
}

#Config related functions lole
#Generates new config and writes it. Returns nothing
def generateNewConfig(config):
	config["config"] = defaultConfig
	
	with open("config.ini", "w") as file:
		config.write(file)

#Tries to set a temporary variable to a key/entry/whatever, sets variable to default key and default key to config if an error is thrown, and then returns that variable
def tryConfigEntry(config, configFile, entry):
	try:
		returnVar = config["config"][entry]
	except KeyError:
		print(entry + " is not in the config; relying on default and writing default to current config...")
		
		returnVar = defaultConfig[entry]
		
		config["config"][entry] = returnVar
		with open(configFile, "w") as file:
			config.write(file)
		
	return returnVar
	
#List-filtering related functions
#Goes through input list and, based on leniency, returns entries that comply with tags, and also deletes any with tags in the blacklist, then returns the filtered list
def filterList(simageList, tags, leniency, blacklist):
	tempList = []
	
	#When it accepts any entry that matches at least 1 tag
	if leniency == 0:
		for i in simageList:
			#Because the entry looks like "id,tags tags tags.jpg", and I need purely the tags
			for j in i.split(".")[0].split(",")[1].split(" "):
				if j in blacklist:
					break
				
				if tags[0] == "any":
					tempList.append(i)
					break
				
				if j in tags:
					tempList.append(i)
					break
	#When it accepts entries that fulfil all tags
	else:
		for i in simageList:
			simageTags = i.split(".")[0].split(",")[1].split(" ")
			
			append = True
			
			for j in tags:
				if j in blacklist:
					append = False
					break
			
				if tags[0] == "any":
					append = True
					break
					
				if j not in simageTags:
					append = False
					break
					
			if append:
				tempList.append(i)
	
	return tempList
	
#Image-related functions
#Tints image and returns
def image_tint(src, tint='#ffffff'):
    if Image.isStringType(src):  # file path?
        src = Image.open(src)
    if src.mode not in ['RGB', 'RGBA']:
        raise TypeError('Unsupported source image mode: {}'.format(src.mode))
    src.load()

    tr, tg, tb = getrgb(tint)
    tl = getcolor(tint, "L")  # tint color's overall luminosity
    if not tl: tl = 1  # avoid division by zero
    tl = float(tl)  # compute luminosity preserving tint factors
    sr, sg, sb = map(lambda tv: tv/tl, (tr, tg, tb))  # per component
                                                      # adjustments
    # create look-up tables to map luminosity to adjusted tint
    # (using floating-point math only to compute table)
    luts = (tuple(map(lambda lr: int(lr*sr + 0.5), range(256))) +
            tuple(map(lambda lg: int(lg*sg + 0.5), range(256))) +
            tuple(map(lambda lb: int(lb*sb + 0.5), range(256))))
    l = grayscale(src)  # 8-bit luminosity version of whole image
    if Image.getmodebands(src.mode) < 4:
        merge_args = (src.mode, (l, l, l))  # for RGB verion of grayscale
    else:  # include copy of src image's alpha layer
        a = Image.new("L", src.size)
        a.putdata(src.getdata(3))
        merge_args = (src.mode, (l, l, l, a))  # for RGBA verion of grayscale
        luts += tuple(range(256))  # for 1:1 mapping of copied alpha values

    return Image.merge(*merge_args).point(luts)
	
#Template functions?
#Returns an unused template from the list and replenishes unused list should it start to run short
def unusedTemplate(unusedList, templatesList, templatesLocation):
	#If the unused list is at 10% or lower the length of the normal templates list, replace unusedList and 
	if len(unusedList) <= round(len(templatesList) * 0.1):
		temporaryList = templatesList
	else:
		temporaryList = unusedList
		
	#Get random index, assign variable to list at that index, and delete that entry within the list
	randomIndex = random.randrange(len(temporaryList))
	
	randomElement = temporaryList[randomIndex]
	
	temporaryList.pop(randomIndex)
		
	return [temporaryList, templatesLocation + "/" + randomElement]

#Meme functions?
#Generates image with stuff and returns
def generateMeme(templateFilename, simagesList, simagesLocation):
	#Go through simages directory and filter through according to what region(s) specif(y|ies)
		
	#Open template image to prepare overlaying simages on it
	templateImageFile = Image.open(templateFilename)
	
	#Get template data (i.e. filename sans extension and path)
	templateText = templateFilename.split("\\")[-1].split("/")[-1].split(".")[0]
	
	useNext = ""
	for entry in templateText.split(";"):
		if entry != "":
			#There are 5 sub-entries: tags, tag leniency, tag blacklist, ul-corner, and lr-corner
			subentries = entry.split(",")
			
			#Select random image from on a list filtered based on some rules (or uses the same one if that is determined)
			simageName = simagesLocation + "/" + random.choice(filterList(simagesList, subentries[0].split(" "), int(subentries[1]), subentries[2].split(" "))) if useNext == "" else useNext
			simage = Image.open(simageName)
			
			#Optional parameters in template region. We have to deal with them first because cropping and such
			#Colorize and zoom image if specified
			try:
				if subentries[5] != "no":
					bound = 0.125
					w, h = simage.size
					simage = ImageOps.grayscale(simage.crop((round(w * bound), round(h * bound), round(w * (1 - bound)), round(h * (1 - bound)))))
					
					#Do all them colors
					if subentries[5] == "red":
						simage = ImageOps.colorize(simage, (0, 0, 0), (255, 25, 25))
					if subentries[5] == "green":
						simage = ImageOps.colorize(simage, (0, 0, 0), (25, 255, 25))
					if subentries[5] == "blue":
						simage = ImageOps.colorize(simage, (0, 0, 0), (25, 25, 255))
					if subentries[5] == "cyan":
						simage = ImageOps.colorize(simage, (0, 0, 0), (25, 255, 255))
					if subentries[5] == "magenta":
						simage = ImageOps.colorize(simage, (0, 0, 0), (255, 25, 255))
					if subentries[5] == "yellow":
						simage = ImageOps.colorize(simage, (0, 0, 0), (255, 255, 25))
			except IndexError:
				simage = simage.copy()
				
			try:
				if subentries[6] == "same":
					useNext = simageName
			except IndexError:
				useNext = ""
				simage = simage.copy()
				
			#Deal with size and position
			#P1 and P2 entry corners sosrt of thing
			P1 = tuple([int(i) for i in subentries[3].split(" ")])
			P2 = tuple([int(i) for i in subentries[4].split(" ")])
			size = (abs(P1[0] - P2[0]), abs(P1[1] - P2[1]))
			pos = P1
				
			#Resize
			simage = simage.resize(size, resample=Image.BILINEAR)
			
			#Paste image ontop
			templateImageFile.paste(simage, pos)
			simage.close()
	
	return templateImageFile
	
#Misc functions
def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)
	
def main():
	#Arg stuff
	argParser = argparse.ArgumentParser(description = "Churns memes at the speed of sound")
	
	argParser.add_argument("-c", "--config",
							metavar = "file",
							type = str,
							help = "Specify custom config. The default config is in the same directory as the install.")
	
	argParser.add_argument("-sl", "--simages-location",
							metavar = "dir",
							type = str,
							help = "Location for simages")
	
	argParser.add_argument("-tl", "--templates-location",
							metavar = "dir",
							type = str,
							help = "Location for templates")
							
	argParser.add_argument("-uf", "--unused-file",
							metavar = "dir",
							type = str,
							help = "Location for unused files")
							
	argParser.add_argument("-q", "--quality",
							metavar = "int",
							type = int,
							help = "Quality of image from 1 (worst) to 95 (best)")
						
	argParser.add_argument("-co", "--count",
							metavar = "count",
							type = int,
							help = "Specify how many memes you intend to output")
							
	argParser.add_argument("-tf", "--template-file",
							metavar = "file",
							type = str,
							help = "Override choosing random template and supply your own, instead. Used for testing purposes")
	
	argParser.add_argument("output",
							metavar = "out",
							type = str,
							help = "Output file (or directory if you're using count)")
	
	args = argParser.parse_args()
	
	#Set variables from config first; set from args after so that args are prioritized over config
	config = configparser.ConfigParser()
	
	if args.config != None:
		config.read(args.config)
		if config.sections() == [] or "config" not in config.sections():
			print("The config specified does not work. Relying on the default config...")
			useDefaultConfig = True
		else:
			useDefaultConfig = False
			configName = args.config
	else:
		useDefaultConfig = True
	
	if useDefaultConfig:
		configName = "config.ini"
		config.read(configName)
		if config.sections() == [] or "config" not in config.sections():
			print("The default config isn't here. Generating a new one...")
			generateNewConfig(config)
	
	#Set variables, prioritizing args over config
	templatesLocation = args.templates_location if args.templates_location != None else tryConfigEntry(config, configName, "templates")
	
	simagesLocation = args.simages_location if args.simages_location != None else tryConfigEntry(config, configName, "simages")
	
	unusedFile = args.unused_file if args.unused_file != None else tryConfigEntry(config, configName, "unused")
	
	imageQuality = args.quality if args.quality != None else int(tryConfigEntry( config, configName, "image-quality"))
	
	#Search directory for random template and its accompanying data file
	for dirpath, dirpaths, filenames in os.walk(templatesLocation):
		#I can't believe I literally have to do something as stupid as this without having to import another module...
		templatesList = filenames
	
	#Get list of simages
	for dirpath, dirpaths, filenames in os.walk(simagesLocation):
		simagesList = filenames
		
	#Get unused templates
	unusedFileHandle = open(unusedFile, "r")
	unusedList = unusedFileHandle.read().split("\n")
	unusedFileHandle.close()
	
	#Setup template override
	templateOverride = False
	if args.template_file != None:
		templateOverride = True
	
	#Outut just one image
	if args.count == None:
		#No need for extra effort or to remove any elements from the list if we're not using them
		if not templateOverride:
			unusedFunc = unusedTemplate(unusedList, templatesList, templatesLocation)
			unusedList = unusedFunc[0]
		
		templateFile = args.template_file if templateOverride else unusedFunc[1]
		
		generateMeme(templateFile, simagesList, simagesLocation).save(args.output, "jpeg", quality = imageQuality)
	#Generate multiple images
	else:
		outdir = ("." if args.output[0] != "." else "") + args.output + ("/" if args.output[len(args.output) - 1] != "/" else "")
		ensure_dir(outdir)
		
		for i in range(args.count):
			#No need for extra effort or to remove any elements from the list if we're not using them
			if not templateOverride:
				unusedFunc = unusedTemplate(unusedList, templatesList, templatesLocation)
				unusedList = unusedFunc[0]
				
			templateFile = args.template_file if templateOverride else unusedFunc[1]
			
			generateMeme(templateFile, simagesList, simagesLocation).save(outdir + "image" + str(i) + ".jpg", "jpeg", quality = imageQuality)
			print("(" + str(i + 1) + "/" + str(args.count) + ")")
			
	#We wouldn't want to truncate the unused file if we weren't going to add to it...
	if not templateOverride:
		unusedFileHandle = open(unusedFile, "w+")
		unusedFileHandle.write("\n".join(unusedList))
		unusedFileHandle.close()
	
	'''
	GOALS
		Make it so that it generates as many unique images as it can and then stops when it can no longer
	'''

if __name__ == "__main__":
	main()