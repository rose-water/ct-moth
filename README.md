# MDP - Creative Technology I
## Behavior in Motion

---

**Design Brief**

Create an interactive piece that uses one or more servo motors to create something that feels alive. It must be based on research inspiration, where you find an example of something alive that behaves through movement.

This project builds on the previous emotion project ideas. But in this project, the physical movement provides the primary mode of expression. The expressive movement can indicate more than emotion, and can be functional (like looking up), or communicative (like shaking left/right to indicate “no”).

This project needs a strong concept as well as thoughtful design and form making – it is not only about technology. Having wires hanging out all over is not acceptable – you must create an enclosure. In other words, the project should feel finished and refined.

---

**Requirements**

- Have more than one type of movement (this creates a much greater sense of life)
- The servo must be attached to something that it moves
- The movement must be altered based on input from a sensor(s)
- Avoid literal human faces
- Use more than one sensor and/or more than one servo

---

**About**

This robot moth was inspired by real life moths from my mother's garden. Because we were tasked to design a project that made use of servos, the most obvious choice would be to use the servos to drive the wings. The moth has an idle state where its wings are 'twitching' and the motor is vibrating, indicating that the moth is 'hungry' for light. The readings from the photocell are mapped to the speed of the moth's wings flapping as well as the range of movement. When light levels are high, the motor stops buzzing, the wings flap at higher speeds and move with a wider range, and the LEDs light up and blink to indicate the moth is 'feeding.' 

The moth is built with the following components:

- [Adafruit HUZZAH32 - ESP32 Feather Board](https://www.adafruit.com/product/3405)
- 2x Diffuse White LEDs
- Photocell
- Mini Vibrating Motor
- 2x Micro Servos 

The enclosure was made from laser cut illustration board. I modeled the enclosure in Cinema 4D (because it's what I'm most comfortable with at the moment), exported it as an OBJ, then used this Python addon called [Export-Paper-Model-From-Blender](https://github.com/addam/Export-Paper-Model-from-Blender) for [Blender 2.8](https://www.blender.org/download/releases/2-80/). More information can be found [here](https://www.instructables.com/id/Papercraft-With-Blender/) (please note these instructions are for an older version of Blender, but they still apply to the plugin linked above). 

The Export-Paper-Model-From-Blender plugin allows you to export as an SVG, so I did that and created layers in an Illustration file (CS6, not CC) that are ready for laser printing. The OBJ and the AI files are available in the `resources` directory.