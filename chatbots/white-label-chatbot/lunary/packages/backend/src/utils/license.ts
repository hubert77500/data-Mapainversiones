import { Next } from "koa"
import Context from "./koa"

const TWO_HOURS = 2 * 60 * 60 * 1000
const cache = {
  license: {
    // Everything is set to true by default in case there's a problem connecting to the license server
    radarEnabled: true,
    evalEnabled: true,
    samlEnabled: true,
    accessControlEnabled: true,
  },
  lastFetch: TWO_HOURS + 200,
}

async function licenseMiddleware(ctx: Context, next: Next) {
    await next()
}

export default licenseMiddleware
