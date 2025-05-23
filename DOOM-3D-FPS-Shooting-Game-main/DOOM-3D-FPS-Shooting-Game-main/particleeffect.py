class ParticleEffect:
    def __init__(self, game):
        self.game = game
        self.particles = []

    def add_particle(self, pos, color, size, velocity):
        self.particles.append({
            'pos': list(pos),
            'color': color,
            'size': size,
            'velocity': velocity,
            'lifetime': 1.0
        })

    def update(self):
        particles_to_remove = []
        for particle in self.particles:
            particle['pos'][0] += particle['velocity'][0]
            particle['pos'][1] += particle['velocity'][1]
            particle['size'] *= 0.95
            particle['lifetime'] -= 0.02
            if particle['lifetime'] <= 0:
                particles_to_remove.append(particle)
        for particle in particles_to_remove:
            self.particles.remove(particle)

    def draw(self):
        for particle in self.particles:
            pg.draw.circle(self.game.screen, particle['color'], particle['pos'], particle['size'])