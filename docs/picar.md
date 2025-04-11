# Picar Robotics Control System Documentation

## Overview

The Picar robotics control system provides the interface for controlling and managing the Picar robot. It handles motor control, sensor readings, and autonomous navigation capabilities.

## Architecture

```
apis/picar/
├── core/             # Core functionality
│   ├── motor_controller.py
│   ├── sensor_manager.py
│   └── navigation.py
├── tests/           # Test suite
├── config/          # Configuration files
└── utils/          # Utility functions
```

## Key Components

### Motor Controller
- Controls motor movements
- Manages speed and direction
- Handles motor calibration
- Provides safety features

### Sensor Manager
- Reads sensor data
- Processes sensor inputs
- Manages sensor calibration
- Handles error detection

### Navigation System
- Plans robot movements
- Handles obstacle avoidance
- Manages path following
- Provides position tracking

## Usage

### Basic Usage
```python
from picar import MotorController

# Initialize controller
controller = MotorController()

# Move robot
controller.move_forward(speed=50)
controller.turn_left(angle=90)
```

### Sensor Operations
```python
from picar import SensorManager

# Initialize sensor manager
sensors = SensorManager()

# Read sensor data
distance = sensors.get_distance()
line_status = sensors.get_line_status()
```

### Navigation Control
```python
from picar import Navigation

# Initialize navigation
nav = Navigation()

# Set destination
nav.set_destination(x=100, y=100)

# Start navigation
nav.start_navigation()
```

## Integration with Other Components

### Autocoder Integration
- Generates control code
- Creates navigation paths
- Handles sensor configurations
- Manages motor settings

### n8n Integration
- Controls robot remotely
- Monitors robot status
- Handles emergency stops
- Manages data logging

## Configuration

### Environment Variables
- `PICAR_SERIAL_PORT`: Serial port
- `PICAR_BAUD_RATE`: Baud rate
- `PICAR_SENSOR_CONFIG`: Sensor settings
- `PICAR_MOTOR_CONFIG`: Motor settings

### Robot Settings
- Motor calibration
- Sensor thresholds
- Navigation parameters
- Safety limits

## Development

### Adding New Features
1. Create feature branch
2. Update control logic
3. Add tests
4. Update documentation

### Testing
- Unit tests for motor control
- Integration tests with sensors
- Navigation system tests
- Safety feature tests

## Troubleshooting

### Common Issues
1. Motor control problems
2. Sensor reading errors
3. Navigation failures
4. Communication issues

### Solutions
1. Check motor connections
2. Verify sensor calibration
3. Review navigation settings
4. Check communication ports

## Support

For issues and questions:
1. Check documentation
2. Review error logs
3. Contact support 