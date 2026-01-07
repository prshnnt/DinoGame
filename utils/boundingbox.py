import pygame


def load_source(bb_path) -> dict:
    import json
    bb_file = open(bb_path)
    data = json.load(bb_file)
    return data

def load_bb(bb_path):
    data = load_source(bb_path)
    states = data['states']
    animations_bblist = {}
    for i in states:
        temp = []
        for frame_box in data[i]:
            temp.append(frame_box)
        animations_bblist[i] = temp
    return animations_bblist
def get_frame_from_image(image:pygame.Surface,frame_bb,scale):
    frame = pygame.Surface((frame_bb['w'],frame_bb['h'])).convert_alpha()
    frame.blit(image,(0,0),(frame_bb['x'],frame_bb['y'],frame_bb['w'],frame_bb['h']))
    frame = pygame.transform.scale(frame,(frame_bb['w']*scale[0],frame_bb['h']*scale[1])).convert_alpha()
    return frame
def extract_frames(image_path,animation_bblist:dict,scale):
    image = pygame.image.load(image_path).convert_alpha()
    animations = {}
    for i in animation_bblist.keys():
        temp = []
        for frame_bb in animation_bblist[i]:
            temp.append(get_frame_from_image(image , frame_bb,scale))
        animations[i] = temp
    return animations

def load_animation(image_path,bb_path,scale):
    return extract_frames(image_path,load_bb(bb_path),scale)