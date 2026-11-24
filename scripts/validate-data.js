#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const readJson = (filename) => JSON.parse(fs.readFileSync(path.join(__dirname, '..', filename), 'utf8'));
const restaurants = readJson('data/restaurants.json');
const hotels = readJson('data/hotels.json');
const failures = [];
const officialMichelin = (value) => typeof value === 'string' && /^https:\/\/guide\.michelin\.com\//.test(value);
const requireValue = (condition, message) => { if (!condition) failures.push(message); };

requireValue(Array.isArray(restaurants) && restaurants.length === 41, `Expected 41 current-star records; found ${restaurants.length}`);
requireValue(Array.isArray(hotels) && hotels.length > 0, 'Hotel data must be a non-empty array');

const seen = new Set();
const stars = { 1: 0, 2: 0, 3: 0 };
for (const restaurant of restaurants) {
  const label = restaurant.name || '(unnamed restaurant)';
  requireValue(Boolean(restaurant.name && restaurant.city), `${label}: name/city required`);
  const key = `${restaurant.name}|${restaurant.city}`.toLocaleLowerCase();
  requireValue(!seen.has(key), `${label}: duplicate restaurant/city row`);
  seen.add(key);
  requireValue([1, 2, 3].includes(restaurant.stars), `${label}: invalid star tier`);
  if (stars[restaurant.stars] !== undefined) stars[restaurant.stars] += 1;
  requireValue(restaurant.statusYear === 2026, `${label}: expected 2026 status year`);
  requireValue(officialMichelin(restaurant.statusSource), `${label}: missing official MICHELIN status source`);
  requireValue(officialMichelin(restaurant.michelinUrl), `${label}: missing official MICHELIN profile`);
  if (restaurant.hours) requireValue(officialMichelin(restaurant.hoursSource), `${label}: hours lack official MICHELIN source`);
  if (restaurant.pairPrice) requireValue(Boolean(restaurant.menuUrl && restaurant.pairPriceNote), `${label}: price lacks menu source or calculation note`);
}

requireValue(stars[3] === 7 && stars[2] === 7 && stars[1] === 27,
  `Expected local 2026 star counts 7/7/27; found ${stars[3]}/${stars[2]}/${stars[1]}`);
for (const hotel of hotels) {
  const label = hotel.name || '(unnamed hotel)';
  requireValue(Boolean(hotel.name && hotel.area), `${label}: name/area required`);
  requireValue(officialMichelin(hotel.source), `${label}: missing official MICHELIN hotel source`);
  requireValue([1, 2, 3].includes(hotel.keys), `${label}: invalid MICHELIN Key count`);
}

if (failures.length) {
  console.error(`Data validation failed (${failures.length} issue${failures.length === 1 ? '' : 's'}):`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`Validated ${restaurants.length} restaurant rows (${stars[3]} three-star, ${stars[2]} two-star, ${stars[1]} one-star) and ${hotels.length} MICHELIN hotel profiles.`);
}
