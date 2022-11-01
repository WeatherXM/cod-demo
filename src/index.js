import process from 'process'
import { readFile } from 'fs/promises'

async function readJsonFile (path) {
  const file = await readFile(path, 'utf8')
  return JSON.parse(file)
}

function orderBySize (a, b) {
  const x = Object.keys(a).length
  const y = Object.keys(b).length
  return x >= y ? [a, b] : [b, a]
}

function rmse (larger, smaller) {
  const sumsOfSquaredErrors = Object.keys(larger).reduce((acc, key) => {
    const { temperature: t1, humidity: h1, wind_speed: w1 } = larger[key]
    const t2 = smaller[key]?.temperature ?? 0
    const h2 = smaller[key]?.humidity ?? 0
    const w2 = smaller[key]?.wind_speed ?? 0
    return {
      temperature: acc.temperature + Math.pow(t1 - t2, 2),
      humidity: acc.humidity + Math.pow(h1 - h2, 2),
      wind_speed: acc.wind_speed + Math.pow(w1 - w2, 2)
    }
  }, { temperature: 0, humidity: 0, wind_speed: 0 })
  const n = Object.keys(larger).length
  const nulls = n - Object.keys(smaller).length
  return {
    rmse: {
      temperature: Math.sqrt(sumsOfSquaredErrors.temperature / n),
      humidity: Math.sqrt(sumsOfSquaredErrors.humidity / n),
      wind_speed: Math.sqrt(sumsOfSquaredErrors.wind_speed / n)
    },
    nulls
  }
}

async function main () {
  if (process.argv.length !== 4) {
    console.log('Please specify exactly 2 command line arguments: the files with the historical observations and forecasts to parse')
    process.exit(1)
  }
  const [f1, f2] = process.argv.slice(2)
  const [d1, d2] = await Promise.all([readJsonFile(f1), readJsonFile(f2)])
  const [larger, smaller] = orderBySize(d1, d2)
  console.log(rmse(larger, smaller))
}

main()
