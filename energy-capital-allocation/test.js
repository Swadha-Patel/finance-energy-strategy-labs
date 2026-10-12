const assert=require('node:assert/strict');const {energy}=require('./models');
const base=energy();
assert(Math.abs(base.solarNPV+107275.77)<.02);
assert(Math.abs(base.combinedNPV+154714.17)<.02);
assert(Math.abs(base.batteryNPV-(base.combinedNPV-base.solarNPV))<.00001);
assert(base.rows[9].combinedCF<0,'Battery replacement must affect year 10');
assert(energy({price:.30}).solarNPV>base.solarNPV);
assert(energy({discount:.15}).solarNPV<base.solarNPV);
console.log('6 energy model checks passed');
