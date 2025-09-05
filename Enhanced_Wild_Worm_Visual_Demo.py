# ENHANCED WILD WORM GAME - SPECTACULAR VISUAL EDITION 🐍✨
# Enhanced with eye-catching visuals and modern effects

import pygame
import random
import math
import sys
import time
import colorsys
import traceback
import os
import array
from PIL import Image, ImageDraw, ImageFont

# --- Enhanced Visual Constants ---
SCREEN_WIDTH_INIT = 800
SCREEN_HEIGHT_INIT = 600
FPS = 60  # Increased for smoother animations

# Enhanced Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (211, 0, 0)
BRIGHT_RED = (255, 0, 0)
GREEN = (0, 180, 0)
BRIGHT_GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
DARK_BLUE = (0, 0, 100)
BRIGHT_BLUE = (50, 50, 255)
DARK_PURPLE = (80, 0, 80)
BRIGHT_PURPLE = (150, 0, 150)
DARK_CYAN = (0, 80, 80)
BRIGHT_CYAN = (0, 255, 255)
YELLOW = (230, 230, 0)
LIGHT_YELLOW = (255, 255, 150)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREY = (169, 169, 169)
DARK_GREY = (100, 100, 100)
SNAKE_COLOR = (34, 139, 34)
SNAKE_COLOR_DARK = (0, 100, 0)
CAGE_COLOR = (139, 69, 19)

# NEW ENHANCED VISUAL COLORS
NEON_RED = (255, 20, 20)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (20, 20, 255)
NEON_PURPLE = (186, 85, 211)
NEON_CYAN = (0, 255, 255)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 140, 0)
NEON_PINK = (255, 20, 147)
ELECTRIC_BLUE = (125, 249, 255)
LIME_GREEN = (50, 205, 50)
CAGE_GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Enhanced particle colors
ENHANCED_PARTICLE_COLORS = [NEON_RED, NEON_ORANGE, NEON_YELLOW, NEON_GREEN, NEON_BLUE, NEON_PURPLE, NEON_PINK, ELECTRIC_BLUE, WHITE]

# Gradient color sets for stunning backgrounds
GRADIENT_COLORS = {
    'sunset': [(255, 94, 77), (255, 154, 0), (255, 206, 84)],
    'ocean': [(64, 224, 208), (70, 130, 180), (25, 25, 112)],
    'forest': [(34, 139, 34), (107, 142, 35), (173, 255, 47)],
    'cosmic': [(138, 43, 226), (75, 0, 130), (25, 25, 112)],
    'fire': [(255, 69, 0), (255, 140, 0), (255, 215, 0)],
    'electric': [(0, 255, 255), (0, 191, 255), (30, 144, 255)]
}

# Game data
SHAPE_NAMES = ["Square", "Triangle", "Rectangle", "Circle", "Pentagon"]
FRUITS = ["Apple", "Banana", "Orange", "Strawberry", "Grapes"]
VEGETABLES = ["Carrot", "Broccoli", "Tomato", "Cucumber", "Pepper"]

# Game States
STATE_WELCOME = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

# Sound settings
SOUND_ENABLED = True
MUSIC_VOLUME = 0.3
SFX_VOLUME = 0.5

# Initialize Pygame
pygame.init()
pygame.font.init()

# Initialize audio with fallback for headless environments
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    AUDIO_AVAILABLE = True
except pygame.error:
    AUDIO_AVAILABLE = False
    print("Audio not available in this environment - running in silent mode")

# Screen setup
screen_width, screen_height = SCREEN_WIDTH_INIT, SCREEN_HEIGHT_INIT
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Wild Worm 🐍✨ - Enhanced Visual & Audio Edition")
clock = pygame.time.Clock()

# Enhanced fonts
DEFAULT_FONT = "Arial"
try:
    FONT_TITLE = pygame.font.SysFont(DEFAULT_FONT, 72, bold=True)
    FONT_MEDIUM = pygame.font.SysFont(DEFAULT_FONT, 36)
    FONT_SMALL = pygame.font.SysFont(DEFAULT_FONT, 24)
    FONT_TINY = pygame.font.SysFont(DEFAULT_FONT, 16)
    FONT_HUD = pygame.font.SysFont("Impact", 48)
except Exception as e:
    print(f"Font loading error: {e}")
    FONT_TITLE = pygame.font.Font(None, 80)
    FONT_MEDIUM = pygame.font.Font(None, 40)
    FONT_SMALL = pygame.font.Font(None, 30)
    FONT_TINY = pygame.font.Font(None, 20)
    FONT_HUD = pygame.font.Font(None, 55)

# Game variables
game_state = STATE_WELCOME
current_gradient = 'cosmic'
particles = []
background_stars = []
snake_segments = []
snake_direction = (1, 0)
snake_speed = 3
lives = 3
score = 0
request_timer = 0
request_time_limit = 10
snake_request = "Circle"
snake_wobble_angle = 0
project_approach_active = False

# Level data
LEVELS = {
    1: {'target': 3, 'time': 22, 'speed_mult': 1.0},
    2: {'target': 4, 'time': 22, 'speed_mult': 1.1},
    3: {'target': 6, 'time': 16, 'speed_mult': 1.2},
    4: {'target': 8, 'time': 16, 'speed_mult': 1.3},
    5: {'target': 10, 'time': 16, 'speed_mult': 1.4},
}

# --- Enhanced Visual Functions ---
def draw_gradient_background(surface, colors, direction='vertical'):
    """Draw stunning gradient backgrounds with smooth color transitions - optimized version."""
    if len(colors) < 2:
        colors = [colors[0], colors[0]]
    
    height = surface.get_height()
    width = surface.get_width()
    
    # Optimization: Draw gradients in chunks instead of line by line for better performance
    chunk_size = max(1, min(8, height // 75))  # Adaptive chunk size based on screen height
    
    if direction == 'vertical':
        for y in range(0, height, chunk_size):
            end_y = min(y + chunk_size, height)
            segment_size = height / (len(colors) - 1)
            segment_idx = min(int(y / segment_size), len(colors) - 2)
            segment_progress = (y % segment_size) / segment_size
            
            color1 = colors[segment_idx]
            color2 = colors[segment_idx + 1]
            
            r = int(color1[0] + (color2[0] - color1[0]) * segment_progress)
            g = int(color1[1] + (color2[1] - color1[1]) * segment_progress)
            b = int(color1[2] + (color2[2] - color1[2]) * segment_progress)
            
            # Draw a rectangle instead of individual lines for better performance
            pygame.draw.rect(surface, (r, g, b), (0, y, width, end_y - y))
    else:
        chunk_size = max(1, min(8, width // 75))  # Adaptive chunk size
        for x in range(0, width, chunk_size):
            end_x = min(x + chunk_size, width)
            segment_size = width / (len(colors) - 1)
            segment_idx = min(int(x / segment_size), len(colors) - 2)
            segment_progress = (x % segment_size) / segment_size
            
            color1 = colors[segment_idx]
            color2 = colors[segment_idx + 1]
            
            r = int(color1[0] + (color2[0] - color1[0]) * segment_progress)
            g = int(color1[1] + (color2[1] - color1[1]) * segment_progress)
            b = int(color1[2] + (color2[2] - color1[2]) * segment_progress)
            
            # Draw a rectangle instead of individual lines for better performance
            pygame.draw.rect(surface, (r, g, b), (x, 0, end_x - x, height))

def create_spectacular_particle(pos, color):
    """Create enhanced particles with sparkle effects."""
    global particles
    play_particle_sound()  # Add sound effect
    
    # Optimization: Limit total particles to maintain performance
    if len(particles) > 150:  # Maximum particle limit
        particles = particles[-100:]  # Keep only the 100 most recent particles
    
    for _ in range(random.randint(5, 12)):
        speed = random.uniform(2.0, 8.0)
        angle = random.uniform(0, math.pi * 2)
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed
        size = random.uniform(3.0, 10.0)
        lifetime = random.uniform(0.8, 2.5)
        
        if color in ENHANCED_PARTICLE_COLORS:
            particle_color = color
        else:
            r, g, b = color
            r = min(255, max(0, r + random.randint(-30, 30)))
            g = min(255, max(0, g + random.randint(-30, 30)))
            b = min(255, max(0, b + random.randint(-30, 30)))
            particle_color = (r, g, b)
        
        particles.append({
            'pos': [pos[0], pos[1]], 
            'vel': [vel_x, vel_y], 
            'size': size,
            'color': particle_color, 
            'lifetime': lifetime, 
            'total_lifetime': lifetime,
            'sparkle': random.random() < 0.3
        })

def update_particles(dt):
    """Update all particles."""
    global particles
    for particle in particles[:]:
        particle['pos'][0] += particle['vel'][0] * dt * 60
        particle['pos'][1] += particle['vel'][1] * dt * 60
        particle['vel'][1] += 0.1 * dt * 60  # Gravity
        particle['vel'][0] *= 0.98
        particle['vel'][1] *= 0.98
        particle['lifetime'] -= dt
        if particle['lifetime'] <= 0:
            particles.remove(particle)

def draw_enhanced_particles(surface):
    """Draw particles with enhanced visual effects."""
    for particle in particles:
        try:
            opacity = max(0, min(255, int(255 * (particle['lifetime'] / particle['total_lifetime']))))
            color = particle['color']
            size = int(particle['size'])
            if size <= 0: continue
            
            particle_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
            
            # Draw main particle
            pygame.draw.circle(
                particle_surface,
                (color[0], color[1], color[2], opacity),
                (size * 2, size * 2),
                size
            )
            
            # Add sparkle effect
            if particle.get('sparkle', False):
                core_size = max(1, size // 3)
                pygame.draw.circle(
                    particle_surface,
                    (255, 255, 255, min(255, opacity + 50)),
                    (size * 2, size * 2),
                    core_size
                )
                
                # Draw sparkle rays
                for i in range(4):
                    angle = i * math.pi / 2 + particle['lifetime'] * 5
                    ray_length = size * 1.5
                    end_x = size * 2 + math.cos(angle) * ray_length
                    end_y = size * 2 + math.sin(angle) * ray_length
                    pygame.draw.line(
                        particle_surface,
                        (255, 255, 255, opacity // 2),
                        (size * 2, size * 2),
                        (end_x, end_y),
                        2
                    )
            
            surface.blit(
                particle_surface,
                (int(particle['pos'][0] - size * 2), int(particle['pos'][1] - size * 2))
            )
        except Exception as e:
            pass

def draw_enhanced_text(surface, text, pos, font, color=WHITE, center=False, glow=False, pulse=False):
    """Draw text with enhanced effects."""
    try:
        if pulse:
            pulse_factor = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() * 0.005)
            color = tuple(min(255, max(0, int(c * pulse_factor))) for c in color[:3])
        
        text_surface = font.render(str(text), True, color)
        text_rect = text_surface.get_rect()
        
        if center:
            text_rect.center = pos
        else:
            text_rect.topleft = pos
        
        if glow:
            glow_color = tuple(min(255, c + 50) for c in color[:3])
            glow_surface = font.render(str(text), True, glow_color)
            
            for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                glow_rect = glow_surface.get_rect()
                if center:
                    glow_rect.center = (pos[0] + offset[0], pos[1] + offset[1])
                else:
                    glow_rect.topleft = (text_rect.left + offset[0], text_rect.top + offset[1])
                surface.blit(glow_surface, glow_rect)
        
        surface.blit(text_surface, text_rect)
        return text_rect
    except Exception as e:
        return pygame.Rect(pos[0], pos[1], 10, 10)

def draw_animated_border(surface, rect, color, thickness=2, animation_speed=0.1):
    """Draw animated border with moving highlights."""
    time_factor = pygame.time.get_ticks() * animation_speed
    
    pygame.draw.rect(surface, color, rect, thickness)
    
    highlight_color = tuple(min(255, c + 100) for c in color[:3])
    
    perimeter = 2 * (rect.width + rect.height)
    highlight_pos = (time_factor % perimeter) / perimeter
    
    if highlight_pos < 0.25:
        x = rect.left + (highlight_pos * 4) * rect.width
        y = rect.top
        pygame.draw.circle(surface, highlight_color, (int(x), int(y)), thickness * 2)
    elif highlight_pos < 0.5:
        x = rect.right
        y = rect.top + ((highlight_pos - 0.25) * 4) * rect.height
        pygame.draw.circle(surface, highlight_color, (int(x), int(y)), thickness * 2)
    elif highlight_pos < 0.75:
        x = rect.right - ((highlight_pos - 0.5) * 4) * rect.width
        y = rect.bottom
        pygame.draw.circle(surface, highlight_color, (int(x), int(y)), thickness * 2)
    else:
        x = rect.left
        y = rect.bottom - ((highlight_pos - 0.75) * 4) * rect.height
        pygame.draw.circle(surface, highlight_color, (int(x), int(y)), thickness * 2)

def create_background_stars():
    """Create twinkling background stars."""
    global background_stars
    if len(background_stars) < 100:
        for _ in range(100 - len(background_stars)):
            background_stars.append({
                'pos': [random.randint(0, screen_width), random.randint(0, screen_height)],
                'brightness': random.uniform(0.3, 1.0),
                'twinkle_speed': random.uniform(0.001, 0.005)
            })

def draw_background_stars(surface):
    """Draw twinkling background stars."""
    for star in background_stars:
        brightness = star['brightness'] + 0.3 * math.sin(pygame.time.get_ticks() * star['twinkle_speed'])
        brightness = max(0.1, min(1.0, brightness))
        
        color_val = int(255 * brightness)
        color = (color_val, color_val, color_val)
        
        pygame.draw.circle(surface, color, (int(star['pos'][0]), int(star['pos'][1])), 1)

def generate_tone(frequency, duration, sample_rate=22050, volume=0.5):
    """Generate a simple tone sound effect."""
    if not SOUND_ENABLED or not AUDIO_AVAILABLE:
        return None
    
    try:
        frames = int(duration * sample_rate)
        arr = array.array('h')  # 16-bit signed integers
        
        for i in range(frames):
            # Simple sine wave with fade out
            fade = 1.0 - (i / frames) * 0.8  # Gentle fade
            wave = volume * fade * math.sin(2 * math.pi * frequency * i / sample_rate)
            sample = int(wave * 32767)
            arr.append(sample)  # Left channel
            arr.append(sample)  # Right channel
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    except:
        return None

def play_click_sound():
    """Play a click sound effect."""
    if SOUND_ENABLED and AUDIO_AVAILABLE:
        try:
            sound = generate_tone(800, 0.1, volume=SFX_VOLUME * 0.3)
            if sound:
                sound.play()
        except:
            pass

def play_particle_sound():
    """Play a particle creation sound effect."""
    if SOUND_ENABLED and AUDIO_AVAILABLE:
        try:
            sound = generate_tone(1200, 0.05, volume=SFX_VOLUME * 0.2)
            if sound:
                sound.play()
        except:
            pass

def play_life_lost_sound():
    """Play a sound when life is lost."""
    if SOUND_ENABLED and AUDIO_AVAILABLE:
        try:
            sound = generate_tone(200, 0.3, volume=SFX_VOLUME * 0.5)
            if sound:
                sound.play()
        except:
            pass

def play_game_over_sound():
    """Play a game over sound effect."""
    if SOUND_ENABLED and AUDIO_AVAILABLE:
        try:
            # Play a descending tone sequence
            for i, freq in enumerate([400, 300, 200, 150]):
                sound = generate_tone(freq, 0.2, volume=SFX_VOLUME * 0.4)
                if sound:
                    pygame.time.wait(50)  # Small delay between tones
                    sound.play()
        except:
            pass

def toggle_sound():
    """Toggle sound on/off."""
    global SOUND_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED

def draw_enhanced_snake(surface):
    """Draw the snake with enhanced visual effects."""
    global snake_wobble_angle
    
    if not snake_segments:
        return
    
    snake_wobble_angle += 0.1
    
    for i, segment_pos in enumerate(reversed(snake_segments)):
        segment_index = len(snake_segments) - 1 - i
        base_size = 15
        size_reduction = min(5, i // 3)
        segment_size = max(6, base_size - size_reduction)
        
        draw_pos = list(segment_pos)
        if project_approach_active:
            wobble_magnitude = 3 * math.sin(snake_wobble_angle + segment_index * 0.5)
            draw_pos[0] += wobble_magnitude
            draw_pos[1] += wobble_magnitude
            
            # Rainbow effect
            hue = (snake_wobble_angle * 0.1 + segment_index * 0.05) % 1.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
            segment_color = (r, g, b)
            outline_color = BLACK
        else:
            segment_color = SNAKE_COLOR if segment_index % 2 == 0 else SNAKE_COLOR_DARK
            outline_color = SNAKE_COLOR_DARK if segment_index % 2 == 0 else SNAKE_COLOR
        
        pygame.draw.circle(surface, segment_color, (int(draw_pos[0]), int(draw_pos[1])), segment_size)
        pygame.draw.circle(surface, outline_color, (int(draw_pos[0]), int(draw_pos[1])), segment_size, 2)
    
    # Draw enhanced head
    head_pos = list(snake_segments[0])
    head_size = 18
    
    if project_approach_active:
        wobble_magnitude = 3 * math.sin(snake_wobble_angle)
        head_pos[0] += wobble_magnitude
        head_pos[1] += wobble_magnitude
        
        hue = (snake_wobble_angle * 0.1) % 1.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
        head_color = (r, g, b)
        head_outline = BLACK
    else:
        head_color = SNAKE_COLOR
        head_outline = SNAKE_COLOR_DARK
    
    pygame.draw.circle(surface, head_color, (int(head_pos[0]), int(head_pos[1])), head_size)
    pygame.draw.circle(surface, head_outline, (int(head_pos[0]), int(head_pos[1])), head_size, 2)
    
    # Draw enhanced eyes
    eye_offset = head_size * 0.6
    eye_size = 4
    
    dx, dy = snake_direction
    mag = math.hypot(dx, dy)
    if mag > 0:
        dx /= mag
        dy /= mag
    
    eye_base_x = head_pos[0] + dx * eye_offset
    eye_base_y = head_pos[1] + dy * eye_offset
    
    perp_dx, perp_dy = -dy, dx
    eye_offset_side = head_size * 0.3
    
    left_eye_x = int(eye_base_x - perp_dx * eye_offset_side)
    left_eye_y = int(eye_base_y - perp_dy * eye_offset_side)
    right_eye_x = int(eye_base_x + perp_dx * eye_offset_side)
    right_eye_y = int(eye_base_y + perp_dy * eye_offset_side)
    
    pygame.draw.circle(surface, WHITE, (left_eye_x, left_eye_y), eye_size)
    pygame.draw.circle(surface, WHITE, (right_eye_x, right_eye_y), eye_size)
    
    pupil_size = 2
    pupil_offset = 1
    pygame.draw.circle(surface, BLACK, (int(left_eye_x + dx*pupil_offset), int(left_eye_y + dy*pupil_offset)), pupil_size)
    pygame.draw.circle(surface, BLACK, (int(right_eye_x + dx*pupil_offset), int(right_eye_y + dy*pupil_offset)), pupil_size)

def draw_enhanced_cage(surface):
    """Draw an enhanced cage with golden accents."""
    cage_rect = pygame.Rect(screen_width//2 - 200, screen_height//2 - 150, 400, 300)
    cage_thickness = 8
    
    # Draw main cage
    pygame.draw.rect(surface, CAGE_COLOR, cage_rect, cage_thickness, border_radius=5)
    
    # Add golden highlights
    highlight_rect = cage_rect.inflate(4, 4)
    pygame.draw.rect(surface, CAGE_GOLD, highlight_rect, 2, border_radius=7)
    
    # Draw animated border
    draw_animated_border(surface, cage_rect, CAGE_GOLD, 1, 0.02)
    
    return cage_rect

def draw_welcome_screen(surface):
    """Draw enhanced welcome screen."""
    global current_gradient
    
    # Draw gradient background
    draw_gradient_background(surface, GRADIENT_COLORS[current_gradient])
    
    # Draw background stars
    draw_background_stars(surface)
    
    # Draw title with effects
    title_text = "Wild Worm 🐍✨"
    hue = (pygame.time.get_ticks() / 3000) % 1.0
    title_color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.8, 1.0))
    
    draw_enhanced_text(surface, title_text, (screen_width // 2, screen_height // 4), 
                      FONT_TITLE, title_color, center=True, glow=True, pulse=True)
    
    # Draw instructions
    draw_enhanced_text(surface, "Enhanced Visual & Audio Edition", (screen_width // 2, screen_height // 4 + 80), 
                      FONT_MEDIUM, NEON_CYAN, center=True, glow=True)
    
    draw_enhanced_text(surface, "Click to Start!", (screen_width // 2, screen_height // 2), 
                      FONT_MEDIUM, WHITE, center=True, pulse=True)
    
    draw_enhanced_text(surface, "Press SPACE to toggle Project Approach", (screen_width // 2, screen_height // 2 + 60), 
                      FONT_SMALL, NEON_YELLOW, center=True)
    
    draw_enhanced_text(surface, "Press G to cycle gradient backgrounds", (screen_width // 2, screen_height // 2 + 100), 
                      FONT_SMALL, NEON_GREEN, center=True)
    
    sound_status = "ON" if SOUND_ENABLED and AUDIO_AVAILABLE else "OFF" if AUDIO_AVAILABLE else "N/A"
    draw_enhanced_text(surface, f"Press S to toggle sound [{sound_status}]", (screen_width // 2, screen_height // 2 + 140), 
                      FONT_SMALL, NEON_CYAN, center=True)
    
    # Draw particles
    draw_enhanced_particles(surface)

def draw_playing_screen(surface):
    """Draw enhanced playing screen."""
    global current_gradient
    
    # Draw gradient background
    draw_gradient_background(surface, GRADIENT_COLORS[current_gradient])
    
    # Draw background stars
    draw_background_stars(surface)
    
    # Draw HUD
    draw_enhanced_text(surface, f"Lives: {lives}", (20, 20), FONT_HUD, NEON_RED, glow=True)
    draw_enhanced_text(surface, f"Score: {score}", (20, 70), FONT_HUD, NEON_GREEN, glow=True)
    
    # Draw request
    request_text = f"Feed me: {snake_request}"
    draw_enhanced_text(surface, request_text, (screen_width // 2, 30), FONT_MEDIUM, NEON_YELLOW, center=True, glow=True)
    
    # Draw timer bar
    timer_width = 300
    timer_height = 20
    timer_x = (screen_width - timer_width) // 2
    timer_y = 70
    
    fill_ratio = request_timer / request_time_limit if request_time_limit > 0 else 0
    fill_width = int(fill_ratio * timer_width)
    
    timer_color = NEON_GREEN if fill_ratio > 0.5 else NEON_ORANGE if fill_ratio > 0.25 else NEON_RED
    
    pygame.draw.rect(surface, DARK_GREY, (timer_x, timer_y, timer_width, timer_height), border_radius=10)
    if fill_width > 0:
        pygame.draw.rect(surface, timer_color, (timer_x, timer_y, fill_width, timer_height), border_radius=10)
    
    draw_animated_border(surface, pygame.Rect(timer_x, timer_y, timer_width, timer_height), WHITE, 2, 0.05)
    
    # Draw cage
    cage_rect = draw_enhanced_cage(surface)
    
    # Draw snake
    draw_enhanced_snake(surface)
    
    # Draw particles
    draw_enhanced_particles(surface)
    
    # Mode indicator
    if project_approach_active:
        draw_enhanced_text(surface, "PROJECT APPROACH MODE", (screen_width // 2, screen_height - 30), 
                          FONT_SMALL, NEON_PINK, center=True, glow=True, pulse=True)

def draw_game_over_screen(surface):
    """Draw enhanced game over screen."""
    # Draw gradient background
    draw_gradient_background(surface, GRADIENT_COLORS['fire'])
    
    # Draw background stars
    draw_background_stars(surface)
    
    # Draw game over text
    draw_enhanced_text(surface, "GAME OVER", (screen_width // 2, screen_height // 3), 
                      FONT_TITLE, NEON_RED, center=True, glow=True, pulse=True)
    
    draw_enhanced_text(surface, f"Final Score: {score}", (screen_width // 2, screen_height // 2), 
                      FONT_MEDIUM, WHITE, center=True, glow=True)
    
    draw_enhanced_text(surface, "Click to restart", (screen_width // 2, screen_height * 3 // 4), 
                      FONT_SMALL, NEON_YELLOW, center=True, pulse=True)
    
    # Draw particles
    draw_enhanced_particles(surface)

def reset_game():
    """Reset game variables."""
    global lives, score, request_timer, snake_segments, game_state
    lives = 3
    score = 0
    request_timer = request_time_limit
    snake_segments = [(screen_width//2, screen_height//2 + i*20) for i in range(5)]
    game_state = STATE_PLAYING

def update_game(dt):
    """Update game logic."""
    global request_timer, lives, game_state, snake_segments
    
    if game_state == STATE_PLAYING:
        request_timer -= dt
        if request_timer <= 0:
            lives -= 1
            play_life_lost_sound()  # Add sound effect for life loss
            request_timer = request_time_limit
            if lives <= 0:
                game_state = STATE_GAME_OVER
                play_game_over_sound()  # Add sound effect for game over
        
        # Move snake
        if snake_segments:
            head_x, head_y = snake_segments[0]
            new_head_x = head_x + snake_direction[0] * snake_speed
            new_head_y = head_y + snake_direction[1] * snake_speed
            
            # Keep snake in bounds
            new_head_x = max(50, min(screen_width - 50, new_head_x))
            new_head_y = max(150, min(screen_height - 50, new_head_y))
            
            snake_segments.insert(0, (new_head_x, new_head_y))
            if len(snake_segments) > 5:
                snake_segments.pop()

def handle_events():
    """Handle pygame events."""
    global running, game_state, current_gradient, project_approach_active
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_SPACE:
                project_approach_active = not project_approach_active
                create_spectacular_particle((screen_width//2, screen_height//2), NEON_PURPLE)
            elif event.key == pygame.K_g:
                gradients = list(GRADIENT_COLORS.keys())
                current_idx = gradients.index(current_gradient)
                current_gradient = gradients[(current_idx + 1) % len(gradients)]
                create_spectacular_particle((screen_width//2, screen_height//2), NEON_CYAN)
            elif event.key == pygame.K_s:
                toggle_sound()
                create_spectacular_particle((screen_width//2, screen_height//2), NEON_YELLOW)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_click_sound()  # Add click sound effect
            if game_state == STATE_WELCOME:
                reset_game()
            elif game_state == STATE_GAME_OVER:
                game_state = STATE_WELCOME
            elif game_state == STATE_PLAYING:
                # Create particle effect on click
                create_spectacular_particle(pygame.mouse.get_pos(), random.choice(ENHANCED_PARTICLE_COLORS))
        
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            background_stars = []  # Regenerate stars for new screen size
    
    return True

# Main game loop
def main():
    """Main game loop."""
    global running, dt
    
    # Initialize background elements
    create_background_stars()
    
    # Create initial particle burst
    for _ in range(20):
        create_spectacular_particle(
            (random.randint(0, screen_width), random.randint(0, screen_height)),
            random.choice(ENHANCED_PARTICLE_COLORS)
        )
    
    running = True
    
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        running = handle_events()
        if not running:
            break
        
        update_particles(dt)
        update_game(dt)
        
        # Draw everything
        if game_state == STATE_WELCOME:
            draw_welcome_screen(screen)
        elif game_state == STATE_PLAYING:
            draw_playing_screen(screen)
        elif game_state == STATE_GAME_OVER:
            draw_game_over_screen(screen)
        
        # Add random ambient particles
        if random.random() < 0.02:
            create_spectacular_particle(
                (random.randint(0, screen_width), random.randint(0, screen_height)),
                random.choice(ENHANCED_PARTICLE_COLORS)
            )
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("🐍✨ Starting Enhanced Wild Worm Game ✨🐍")
    print("Features:")
    print("- Spectacular gradient backgrounds")
    print("- Enhanced particle effects with sparkles")
    print("- Animated borders and text effects")
    print("- Twinkling star field")
    print("- Rainbow snake mode")
    print("- Neon color palette")
    print("- Smooth 60 FPS animations")
    print("- Dynamic sound effects and audio feedback")
    print("\nControls:")
    print("- Click to interact")
    print("- SPACE: Toggle Project Approach mode")
    print("- G: Cycle gradient backgrounds")
    print("- S: Toggle sound effects")
    print("- ESC: Exit")
    print(f"\nAudio Status: {'Available' if AUDIO_AVAILABLE else 'Not Available (Silent Mode)'}")
    print("Enjoy the enhanced visuals and audio! 🎮✨🔊")
    
    main()