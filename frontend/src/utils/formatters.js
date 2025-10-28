export const formatDegree = (degree, minute, second = 0) => {
  return `${degree}° ${minute}' ${second}"`;
};

export const formatPlanetPosition = (planetData) => {
  if (!planetData) return 'N/A';
  const { zodiacSign, degree, minute } = planetData;
  return `${zodiacSign} ${formatDegree(degree, minute)}`;
};

export const formatAspect = (aspect) => {
  const { planet1, planet2, aspect: aspectType, orb, symbol } = aspect;
  return `${planet1} ${symbol} ${planet2} (orb: ${orb}°)`;
};

export const getHouseSystemName = (code) => {
  const systems = {
    'P': 'Placidus',
    'K': 'Koch',
    'W': 'Whole Sign',
    'E': 'Equal',
    'R': 'Regiomontanus',
    'C': 'Campanus',
    'T': 'Topocentric'
  };
  return systems[code] || code;
};
