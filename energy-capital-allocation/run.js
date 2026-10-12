const {energy}=require('./models');
const price=process.argv[2]===undefined?.14:Number(process.argv[2]);
if(!Number.isFinite(price)||price<0)throw Error('Energy price must be finite and nonnegative');
console.log(JSON.stringify(energy({price}),null,2));
