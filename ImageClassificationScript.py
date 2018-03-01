import sys
from colorama import init
init()
from colorama import Fore, Back, Style
import os.path
from pci.api import datasource as ds

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)


#Getting file path from the script parameters
paramsLen = len(sys.argv)
if paramsLen > 1:
    fileParam = sys.argv[1]
    if os.path.exists(fileParam):
        if fileParam.lower().endswith(".pix"):
            print "Pix file path: " + Style.BRIGHT + Fore.GREEN + fileParam + Style.RESET_ALL
        else: sys.exit("{0}{1}The file ({2}) is not a PIX file!".format(Style.BRIGHT, Fore.RED, fileParam))
    else: sys.exit(Style.BRIGHT + Fore.RED + "The file ("+ fileParam +") does not exist!")
else:
    sys.exit(Style.BRIGHT + Fore.RED +"A Pix file is expected as a script parameter!")

with ds.open_dataset(fileParam, ds.eAM_READ) as pix:
    numberOfChannels = pix.chan_count
#    print("Number of channels = {0}".format(chans))

#prompting for input channels
inputChanelsParam = raw_input("Please enter the input channels as comma separated numbers or just hit enter for the default (1,2,3,4,5,6) :\n").strip()
if inputChanelsParam == '':
    inputChanelsParam = [1,2,3,4,5,6]
else:
    inputChanelsParamArr = []
    inputChanelsSplitted = inputChanelsParam.split(',')
    count = 0;
    while count < len(inputChanelsSplitted):
        if inputChanelsSplitted[count].isdigit():
            newInt = int(inputChanelsSplitted[count])
            if newInt > numberOfChannels:
                sys.exit(Style.BRIGHT + Fore.RED + "{0} is greater than the channels in the file ({1} channels)!".format(newInt, numberOfChannels))
            count = count + 1
            inputChanelsParamArr.append(newInt)
        else:
            print "Wrong input for input channels, exiting..."
            sys.exit(Style.BRIGHT + Fore.RED + "Input channels were not in the correct format!")
        inputChanelsParam = inputChanelsParamArr
print "Input channels: " + Style.BRIGHT + Fore.GREEN + ",".join(str(e) for e in inputChanelsParam) + Style.RESET_ALL
print ""
print ""


#prompting for output channel
message = "Please enter the offset output channel number "+ Style.BRIGHT + Fore.YELLOW +\
"\nNOTE: This script needs three channels to do its work, if you enter for example 8, the script work on channels 8, 9 and 10, will create them if necassary, if you do not provide a value for this parameter the script will create new channels and append to the file" + Style.RESET_ALL+":\n"
outputOffsetChannelParam = raw_input(message).strip()
if outputOffsetChannelParam == '':
    outputOffsetChannelParam = numberOfChannels + 1
    #sys.exit(Style.BRIGHT + Fore.RED + "Output classification channel was not provided!")
elif outputOffsetChannelParam.isdigit():
    outputOffsetChannelParam = int(outputOffsetChannelParam)
else :
    sys.exit(Style.BRIGHT + Fore.RED + "Output offset channel was not in the correct format!")
# if(outputOffsetChannelParam > 13):
#     sys.exit("{0}{1}Channels in Pix cannot exceed 15 channels!".format(Style.BRIGHT, Fore.RED))

print "Output offset channels: {0}{1}{2}, {3} and {4}{5}".format(Style.BRIGHT, Fore.GREEN, str(outputOffsetChannelParam), str(outputOffsetChannelParam+1), str(outputOffsetChannelParam+2), Style.RESET_ALL)
print ""
print ""


#prompting for number of classes
numOfClassesParam = raw_input("Please enter the number of classification classes or just hit enter for the default (5):\n").strip()
if numOfClassesParam == '':
    numOfClassesParam = 5
elif numOfClassesParam.isdigit():
    numOfClassesParam = int(numOfClassesParam)
else :
    sys.exit(Style.BRIGHT + Fore.RED + "Number of classification classes was not in the correct format!")
print "Number of classes: "+ Style.BRIGHT + Fore.GREEN + str(numOfClassesParam) + Style.RESET_ALL
print ""
print ""


#prompting for number of iterations
numOfIterations = raw_input("Please enter the number of K-Means iterations or just hit enter for the default (5):\n").strip()
if numOfIterations == '':
    numOfIterations = 5
elif numOfIterations.isdigit():
    numOfIterations = int(numOfIterations)
else :
    sys.exit(Style.BRIGHT + Fore.RED + "Number of K-Means iterations was not in the correct format!")
print "Number of K-means iterations: " + Style.BRIGHT + Fore.GREEN + str(numOfIterations) +Style.RESET_ALL
print ""
print ""


#prompting for chanel type
 #add 0 8bit, 0 16bit signed, 1 16bit unsigned and 0 32bit real channels
channelType = raw_input("Please specify the channel type, enter 1 for 8 bit, 2 for 16 bit signed, 3 for 16 bits unsigned or 4 for 32 bit real channel or nothing for the default (16 bit unsigned):\n").strip()
if channelType == '':
    channelType = 3
elif channelType.isdigit():
    channelType = int(channelType)
else :
    sys.exit(Style.BRIGHT + Fore.RED + "Channel type was not in the correct format!")
if channelType == 1:
    channelTypeString = "8 bit"
elif channelType == 2:
    channelTypeString = "16 bit signed"
elif channelType == 3:
    channelTypeString = "16 bits unsigned"
elif channelType == 4:
    channelTypeString = "32 bit real"
else:
    sys.exit(Style.BRIGHT + Fore.RED + "Channel type was not in the correct format!")
print "Channel type: " + Style.BRIGHT + Fore.GREEN + channelTypeString +Style.RESET_ALL
print ""
print ""

#prompting for FMO
fmoFilterSize = raw_input("Please enter the FMO filter size as comma separated numbers or just hit enter for the default (5,5)\nNote:Input Should be in format i, j where i and j are odd integers between 1 and 7, inclusively! :\n").strip()
if fmoFilterSize == '':
    fmoFilterSize = [5,5]
else:
    fmoFilterSizeArr = []
    inputChanelsSplitted = fmoFilterSize.split(',')
    count = 0;
    if len(inputChanelsSplitted) > 2:
        sys.exit(Style.BRIGHT + Fore.RED + "FMO filter size should be only 2 comma separated values!")
    while count < len(inputChanelsSplitted):
        if inputChanelsSplitted[count].isdigit():
            newInt = int(inputChanelsSplitted[count])
            if(newInt < 1 or newInt > 7 or newInt % 2 == 0):
                sys.exit(Style.BRIGHT + Fore.RED + "FMO filter size: should be in format i, j where i and j are odd integers between 1 and 7, inclusively!")
            count = count + 1
            fmoFilterSizeArr.append(newInt)
        else:
            print "Wrong input for FMO filter size, exiting..."
            sys.exit(Style.BRIGHT + Fore.RED + "FMO filter size was not in the correct format!")
        fmoFilterSize = fmoFilterSizeArr
print "FMO filter siz: " + Style.BRIGHT + Fore.GREEN + ",".join(str(e) for e in fmoFilterSize) + Style.RESET_ALL
print ""
print ""


#prompting for SIEVE polygon size threshold
sievePolygonSizeThreshold = raw_input("Please enter the SIEVE filter polygon size threshold or just hit enter for the default (6):\n").strip()
if sievePolygonSizeThreshold == '':
    sievePolygonSizeThreshold = 6
elif sievePolygonSizeThreshold.isdigit():
    sievePolygonSizeThreshold = int(sievePolygonSizeThreshold)
else :
    sys.exit(Style.BRIGHT + Fore.RED + "SIEVE filter polygon size threshold was not in the correct format!")
print "SIEVE filter polygon size threshold: " + Style.BRIGHT + Fore.GREEN + str(sievePolygonSizeThreshold) +Style.RESET_ALL
print ""
print ""


#prompting for SIEVE polygon size threshold
sievePolygonConnectedness = raw_input("Please enter the SIEVE polygon connectedness rule, enter 4 for 4-connected polygons rule, or 8 for 8-connected polygons rule or just hit enter for the default (4 connectedness rule):\n").strip()
if sievePolygonConnectedness == '':
    sievePolygonConnectedness = 4
elif sievePolygonConnectedness.isdigit():
    sievePolygonConnectedness = int(sievePolygonConnectedness)
else :
    sys.exit(Style.BRIGHT + Fore.RED + "SIEVE polygon connectedness rule was not in the correct format!")
print "SIEVE polygon connectedness rule: " + Style.BRIGHT + Fore.GREEN + str(sievePolygonConnectedness) +Style.RESET_ALL



if(outputOffsetChannelParam > numberOfChannels):
    print ("{0}{1}Adding Channel number {2} to the Pix file for unsupervised classification results{3}".format(Style.BRIGHT, Fore.GREEN, outputOffsetChannelParam, Style.RESET_ALL))
    from pci.pcimod import pcimod
    channels = [0,0,0,0]
    channels[channelType - 1] = 1
    #channels = [0,0,1,0] #add 0 8bit, 0 16bit signed, 1 16bit unsigned and 0 32bit real channels
    pcimod(fileParam, "ADD", channels)

file	=	fileParam
dbic	=	inputChanelsParam	# input channels
dboc	=	[outputOffsetChannelParam]	# output channel
mask	=	[]	# process entire image
numclus	=	[numOfClassesParam]	# requested number of clusters
seedfile	=	''	#  automatically generate seeds
maxiter	=	[numOfIterations]	# no more than 20 iterations
movethrs	=	[0.01]
#Write a summary of parameters
print ("{0}{1}Executing unsupervised classification on file: {2}{3}\nParams=>\nInput channels: {4}\nOutput classification channel: {5}\nNumber of classes: {6}\n" + \
    "Number of numOfIterations: {7}\nPlease wait this may take a minute ....{8}") \
    .format(Style.BRIGHT, Fore.GREEN, fileParam, Fore.BLUE, inputChanelsParam, outputOffsetChannelParam, numOfClassesParam, numOfIterations, Style.RESET_ALL)
from pci.kclus import kclus
kclus( file, dbic, dboc, mask, numclus, seedfile, maxiter, movethrs)
#print "{0}{1}Unsupervised classification has executed!\nExecuting FMO filter ... {2}".format(Style.BRIGHT, Fore.BLUE, Style.RESET_ALL);



if(outputOffsetChannelParam + 1 > numberOfChannels):
    print ("{0}{1}Adding Channel number {2} to the Pix file for FMO results{3}".format(Style.BRIGHT, Fore.GREEN, outputOffsetChannelParam + 1, Style.RESET_ALL))
    from pci.pcimod import pcimod
    # channels = [0,0,1,0] #add 0 8bit, 0 16bit signed, 1 16bit unsigned and 0 32bit real channels
    channels = [0,0,0,0]
    channels[channelType - 1] = 1
    pcimod(fileParam, "ADD", channels)

outputFMOChannel = outputOffsetChannelParam + 1;
flsz		=	fmoFilterSize	# Specifies a 5x5 filter size
mask		=	[]		# Processes the entire database
thinline	=	"OFF"	# Does not preserve thin lines
keepvalu	=	[]
bgzero		=	"YES"
print ("{0}{1}Executing FMO on file: {2}{3}\nParams=>\nInput channel: {4}\nOutput FMO channel: {5}\nFilter Size: {6}\n" + \
    "Preserve Thin Lines: {7}\nPlease wait this may take a minute ....{8}") \
    .format(Style.BRIGHT, Fore.GREEN, fileParam, Fore.BLUE, outputOffsetChannelParam, outputFMOChannel, ",".join(str(e) for e in flsz), thinline, Style.RESET_ALL)
from pci.fmo import *
fmo( file, [outputOffsetChannelParam], [outputFMOChannel], flsz, mask, thinline, keepvalu, bgzero )

#sys.exit("temp exit after FMO!")

if(outputOffsetChannelParam + 2 > numberOfChannels):
    print ("{0}{1}Adding Channel number {2} to the Pix file for SIEVE filter results{3}".format(Style.BRIGHT, Fore.GREEN, outputOffsetChannelParam + 2, Style.RESET_ALL))
    from pci.pcimod import pcimod
    # channels = [0,0,1,0] #add 0 8bit, 0 16bit signed, 1 16bit unsigned and 0 32bit real channels
    channels = [0,0,0,0]
    channels[channelType - 1] = 1
    pcimod(fileParam, "ADD", channels)

outputSieveChannel = outputFMOChannel + 1;
sthresh	=	[sievePolygonSizeThreshold]	# polygon size threshold
keepvalu	=	[]	# no keep value
connect	=	[sievePolygonConnectedness]	# default, 4-connection
print ("{0}{1}Executing SIEVE Filter on file: {2}{3}\nParams=>\nInput channel: {4}\nOutput SIEVE Filter channel: {5}\nPolygon threshold(maximum) Size: {6}\n" + \
    "Polygon Connectedness rule: {7}\nPlease wait this may take a minute ....{8}") \
    .format(Style.BRIGHT, Fore.GREEN, fileParam, Fore.BLUE, outputFMOChannel, outputSieveChannel, sievePolygonSizeThreshold,str(sievePolygonConnectedness) , Style.RESET_ALL)

from pci.sieve import *
sieve( file, [outputFMOChannel], [outputSieveChannel], sthresh, keepvalu, connect )



print ("{0}{1}Executing Ras2Poly on file: {2}{3}\nPlease wait this may take a minute ....{4}") \
    .format(Style.BRIGHT, Fore.GREEN, fileParam, Fore.BLUE, Style.RESET_ALL)

from os.path import basename, dirname, join
dbic     = [outputSieveChannel]
dirname = os.path.dirname(file)
filename = os.path.basename(file)
filenameparts = filename.split('.')
extension = filenameparts[1]
filenameWithoutExt = filenameparts[0]
shapefileDirectoryName = filenameWithoutExt + "_shapefile"
shapefileName = filenameWithoutExt + ".shp"
count = 0
if not os.path.exists(os.path.join(dirname, shapefileDirectoryName)):
    os.makedirs(os.path.join(dirname, shapefileDirectoryName))
else:
    shapefileDirectoryNameNew = shapefileDirectoryName + "_" + str(count)
    while os.path.exists(os.path.join(dirname, shapefileDirectoryNameNew)):
        shapefileDirectoryNameNew = shapefileDirectoryName + "_" + str(count)
        count = count + 1
    os.makedirs(os.path.join(dirname, shapefileDirectoryNameNew))
filo = os.path.join(dirname, shapefileDirectoryNameNew, shapefileName)
#extIndex = file.lower().find(".pix")
#filo     = file[:extIndex] + "_Poly" + ".shp"#file[extIndex:]    # output file to be created

fileSuffix = 0;
while os.path.exists(filo):
    filo     = file[:extIndex] + "_Poly_" + str(fileSuffix) + file[extIndex:]
    fileSuffix+=1

smoothv  = ""                # default, YES vectors are smoothed
dbsd     = ""                # defaults to "Created from Raster"
ftype    = "shp"                # default, PIX
foptions = ""                # output format options

from pci.ras2poly import *
ras2poly(file, dbic, filo, smoothv, dbsd, ftype, foptions)

print ("{0}{1}Ras2Poly completed successfully, new file is created: {2}{3}") \
    .format(Style.BRIGHT, Fore.GREEN, filo, Style.RESET_ALL)
