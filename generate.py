#!/usr/bin/python3

remoteName = 'samsungac'

def writeHead() :
    print('[REMOTE]')
    print('  [NAME]' + remoteName)
    print('''
[TIMING]
  [0][N]5[1]472 528[2]488 1496[3]496 3000[4]3000 8968[5]592 15496[RC]1[RP]0[FREQ]39[FREQ-MEAS]
  [1][N]5[1]576 17920[2]504 496[3]496 1496[4]504 2968[5]3000 8960[RC]1[RP]0[FREQ]38[FREQ-MEAS][SB]

[COMMANDS]
  [off][T]0[D]430100000001001101111100000000000000000000000000000000011231000000001001011111100000000000000000000000000000000000023100000000100110011110101100011100000000010001000000000110''')

def getFirstHalf(isQuiet) :
    if isQuiet :
        return "0100000001000001111100000000000000000000000001000000111123"

    return "0100000001001001111100000000000000000000000000000000111123"

def swingBits(swingOnOff) :
    if swingOnOff == 'S' :
        return '010'
    return '111'

def smartSaverBits(flag) :
    if flag == 'S' :
        return '111'
    return '000'

def autoFanBits(func, fanSpeed) :
    if func == 'A' :
        return '011'

    if fanSpeed == 'A' :
        return '000'

    if fanSpeed == 'L' :
        return '010'

    if fanSpeed == 'M' :
        return '001'

    if fanSpeed == 'H' :
        return '101'

    raise Exception('Unexpected fanSpeed:' + fanSpeed)
    return '111'

def funcBits(func) :
    if func == 'C' :
        return '100'
    if func == 'D' :
        return '010'
    if func == 'H' :
        return '001'
    
    return '000'

def getSecondHalf(flag, fanSpeed, swingOnOff, func, temp) :
    beforeChecksum = '100000000100'

    afterChecksum = '111' + swingBits(swingOnOff) + '11' + smartSaverBits(flag)
    afterChecksum += '11100000'
    afterChecksum += ('{0:04b}'.format(temp - 16))[::-1]                # reversed!
    afterChecksum += '1' + autoFanBits(func, fanSpeed)
    afterChecksum += funcBits(func)
    afterChecksum += '0000011110'
    checksum = ('{0:05b}'.format(32 - afterChecksum.count('1')))[::-1]

    return beforeChecksum + checksum + afterChecksum

def writeCode(flag, fanSpeed, swingOnOff, func, temp) :
    if isProhibited(flag, fanSpeed, swingOnOff, func, temp) :
        return

    tempStr = str(temp)

    if func == 'F' :
        tempStr = 'XX'

    commandCode = flag + fanSpeed + swingOnOff + func + tempStr
    print("  [" + commandCode + "][T]1[D]S3" + getFirstHalf(flag == 'Q') + getSecondHalf(flag, fanSpeed, swingOnOff, func, temp))


def isProhibited(flag, fanSpeed, swingOnOff, func, temp) :
    if func == 'F' and temp != 16 :             # fan -> only one entry
        return True

    if func == 'F' and flag != 'N' :            # fan does not allow Quiet or Smart-saver
        return True

    if flag == 'S' and temp < 24 :              # smart saver min temp is 24
        return True

    if func == 'D' and temp < 18 :              # dry min temp is 18
        return True

    if func == 'A' and fanSpeed != 'A' :        # auto means fan is on auto too
        return True

    return False


writeHead()

for flag in ('N', 'Q', 'S') :
    for fanSpeed in ('A', 'L', 'M', 'H') :
        for swingOnOff in ('S', 'N') :
            for func in ('A', 'C', 'D', 'F', 'H') :
                for temp in range(16, 31) :
                    writeCode(flag, fanSpeed, swingOnOff, func, temp)



