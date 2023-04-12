//@deno-types="npm:@types/express"
import express from "npm:express"
import winston from "npm:winston"
import expressWinston from "npm:express-winston"

const app = express()
app.use(expressWinston.logger({
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({
      filename: "/var/log/app/app.log"
    })
  ],
  format: winston.format.combine(
    winston.format.colorize(),
    winston.format.simple()
  ),
  meta: false,
  msg: "HTTP {{req.method}} {{req.url}} {{JSON.stringify(req.body)}}",
  colorize: false,
  
}));


app.use(express.static("."))
app.use(express.json())

app.get("/", (_req, res) => {
  res.sendFile("index.html")
})

app.post("/", async (req, res) => {
  const { url } = req.body
  res.send(await fetch(url)
    .then(res => res.text())
    .catch((err) => err)
  )
})

if (import.meta.main) {
  app.listen(8000, () => {
    console.log("listen @ http://localhost:8000")
  })
}
