const Koa = require('koa')
const Router = require('koa-router')
const Redis = require('ioredis')

const redis = new Redis()

const app = new Koa()
const router = Router({ prefix: '/api' })

router.get('/like/:id', async (ctx, next) => {
    const { id } = ctx.params
    const like = parseInt(await redis.hmget(id, 'like')) || 0
    await redis.hmset(ctx.params.id, { like: like + 1 })
    ctx.body = like + 1
})

router.get('/like', async (ctx, next) => {
    ctx.body = ctx.query.ids.split(',')
})

app.use(async (ctx, next)=> {
    ctx.set('Access-Control-Allow-Origin', '*')
    ctx.set('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild')
    ctx.set('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS')
    ctx.set("Content-Type", "application/json;charset=utf-8")
    await next()
}).use(router.routes()).use(router.allowedMethods())

app.listen(3000)