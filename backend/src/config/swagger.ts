import swaggerJsdoc from 'swagger-jsdoc';

const options: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Mula: The Root API',
      version: '1.0.0',
      description: 'RESTful API for Astrology Synthesis application with birth chart calculations, BMAD analysis, and Symbolon card interpretations',
      contact: {
        name: 'Development Team',
        url: 'https://github.com/Thelastlineofcode/Astrology-Synthesis',
      },
      license: {
        name: 'ISC',
        url: 'https://opensource.org/licenses/ISC',
      },
    },
    servers: [
      {
        url: 'http://localhost:5000',
        description: 'Development server',
      },
      {
        url: 'http://localhost:5000/api/v1',
        description: 'Development server (v1)',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
          description: 'Enter your JWT token in the format: Bearer <token>',
        },
      },
      schemas: {
        User: {
          type: 'object',
          required: ['id', 'email', 'name'],
          properties: {
            id: {
              type: 'string',
              description: 'User ID',
              example: '1234567890',
            },
            email: {
              type: 'string',
              format: 'email',
              description: 'User email address',
              example: 'user@example.com',
            },
            name: {
              type: 'string',
              description: 'User full name',
              example: 'John Doe',
            },
          },
        },
        Chart: {
          type: 'object',
          required: ['id', 'userId', 'name', 'birthDate', 'birthTime', 'latitude', 'longitude'],
          properties: {
            id: {
              type: 'string',
              description: 'Chart ID',
              example: '1234567890',
            },
            userId: {
              type: 'string',
              description: 'User ID who owns the chart',
              example: '1234567890',
            },
            name: {
              type: 'string',
              description: 'Chart name',
              example: 'My Birth Chart',
            },
            birthDate: {
              type: 'string',
              format: 'date',
              description: 'Birth date (ISO 8601)',
              example: '1990-01-15',
            },
            birthTime: {
              type: 'string',
              pattern: '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',
              description: 'Birth time in HH:MM format (24-hour)',
              example: '14:30',
            },
            latitude: {
              type: 'number',
              format: 'float',
              minimum: -90,
              maximum: 90,
              description: 'Birth location latitude',
              example: 40.7128,
            },
            longitude: {
              type: 'number',
              format: 'float',
              minimum: -180,
              maximum: 180,
              description: 'Birth location longitude',
              example: -74.0060,
            },
            createdAt: {
              type: 'string',
              format: 'date-time',
              description: 'Chart creation timestamp',
              example: '2025-10-28T12:00:00.000Z',
            },
          },
        },
        ChartCalculation: {
          type: 'object',
          properties: {
            planets: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  name: {
                    type: 'string',
                    example: 'Sun',
                  },
                  longitude: {
                    type: 'number',
                    example: 295.5,
                  },
                  latitude: {
                    type: 'number',
                    example: 0.0,
                  },
                  sign: {
                    type: 'string',
                    example: 'Capricorn',
                  },
                  house: {
                    type: 'integer',
                    example: 10,
                  },
                  isRetrograde: {
                    type: 'boolean',
                    example: false,
                  },
                },
              },
            },
            houses: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  number: {
                    type: 'integer',
                    example: 1,
                  },
                  longitude: {
                    type: 'number',
                    example: 120.5,
                  },
                  sign: {
                    type: 'string',
                    example: 'Cancer',
                  },
                },
              },
            },
            aspects: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  planet1: {
                    type: 'string',
                    example: 'Sun',
                  },
                  planet2: {
                    type: 'string',
                    example: 'Moon',
                  },
                  aspect: {
                    type: 'string',
                    example: 'Trine',
                  },
                  orb: {
                    type: 'number',
                    example: 2.5,
                  },
                },
              },
            },
          },
        },
        ChartInterpretation: {
          type: 'object',
          properties: {
            chartId: {
              type: 'string',
              example: '1234567890',
            },
            bmadAnalysis: {
              type: 'object',
              properties: {
                personalityProfile: {
                  type: 'object',
                  description: 'BMAD personality analysis',
                },
                behaviorPredictions: {
                  type: 'object',
                  description: 'Predicted behavioral patterns',
                },
              },
            },
            symbolonCards: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  name: {
                    type: 'string',
                    example: 'The Sun',
                  },
                  meaning: {
                    type: 'string',
                    example: 'Core identity and self-expression',
                  },
                  position: {
                    type: 'string',
                    example: 'Capricorn in 10th House',
                  },
                },
              },
            },
            insights: {
              type: 'string',
              description: 'General interpretation insights',
            },
          },
        },
        Error: {
          type: 'object',
          properties: {
            success: {
              type: 'boolean',
              example: false,
            },
            error: {
              type: 'object',
              properties: {
                message: {
                  type: 'string',
                  example: 'Error message',
                },
                statusCode: {
                  type: 'integer',
                  example: 400,
                },
              },
            },
          },
        },
        ValidationError: {
          type: 'object',
          properties: {
            success: {
              type: 'boolean',
              example: false,
            },
            errors: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  field: {
                    type: 'string',
                    example: 'email',
                  },
                  message: {
                    type: 'string',
                    example: 'Valid email is required',
                  },
                },
              },
            },
          },
        },
      },
      responses: {
        UnauthorizedError: {
          description: 'Authentication token is missing or invalid',
          content: {
            'application/json': {
              schema: {
                $ref: '#/components/schemas/Error',
              },
              example: {
                success: false,
                error: {
                  message: 'No token provided',
                  statusCode: 401,
                },
              },
            },
          },
        },
        NotFoundError: {
          description: 'Resource not found',
          content: {
            'application/json': {
              schema: {
                $ref: '#/components/schemas/Error',
              },
              example: {
                success: false,
                error: {
                  message: 'Resource not found',
                  statusCode: 404,
                },
              },
            },
          },
        },
        ValidationError: {
          description: 'Validation error',
          content: {
            'application/json': {
              schema: {
                $ref: '#/components/schemas/ValidationError',
              },
            },
          },
        },
      },
    },
    tags: [
      {
        name: 'Health',
        description: 'Health check endpoints',
      },
      {
        name: 'Authentication',
        description: 'User authentication and authorization',
      },
      {
        name: 'Charts',
        description: 'Birth chart management and operations',
      },
      {
        name: 'Calculations',
        description: 'Chart calculation and interpretation',
      },
    ],
  },
  apis: ['./src/routes/*.ts', './src/index.ts'],
};

export const swaggerSpec = swaggerJsdoc(options);
