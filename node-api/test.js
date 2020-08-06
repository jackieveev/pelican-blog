const Redis = require('ioredis')

const redis = new Redis()

const test = async () => {
    await redis.del('hello')
    await redis.del('you')
    const hello = await redis.get('hello')
    console.log('@@', hello)
}

test()