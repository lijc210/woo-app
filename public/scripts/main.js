;
(function (window) {
    window.requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
        window.webkitRequestAnimationFrame || window.msRequestAnimationFrame

    const FRAME_RATE = 60
    const PARTICLE_NUM = 2000
    const RADIUS = Math.PI * 2
    const CANVASWIDTH = 1000
    const CANVASHEIGHT = 150
    const CANVASID = 'canvas'

    let texts = [
        '不要想念，没有用，要拥抱，要见面。',
        '谈恋爱挺麻烦的，以后就麻烦你啦。',
        // '从前车马书信都很慢，慢到一生，只够爱一个人，现在也是。',
        '一分钟想你想了一秒，剩下的五十九秒都在回味。',
        '你的口红我包了，但以后记得每天还我一点点。',
        '祝你今天愉快，你明天的愉快留着我明天再祝。',
        '哪来这么多情话，我看你的每一个眼神都是表白。',
        '我这个人不算太好，不算太坏，你姑且试试。',
        '想给你直接的拥抱，文字的告白始终差点温度。',
        '我望着月亮，却只看见你。',
        '愿你岁月波澜有人陪，余生悲欢有人听。',
        '什么都可以过期，喜欢我不可以。',
        '醒来觉得甚是爱你。',
        '不要愁老之将至，你老了一定很可爱。',
        '如果我不曾见过你，我本可以忍受孤独。',
        '不须耳鬓常厮伴，一笑低头意已倾。',
        // '三餐，四季，不必太匆忙，毕竟我有一生的时间要和你浪费。',
        // '以后我不养猫，不养狗，只养你，毕竟养猪可以发家致富。',
        '感情不是找一个最好的人，而是找一个对你最好的人。',
        // '人分为两类，是你和不是你。时间分两类，你在的时候和你不在的时候。',
        // '奥利奥的打开方式是舔一舔再泡一泡，你的打开方式是不是亲一亲再抱一抱。',
        '如果有个人对你特别好，记得千万别把那个人弄丢了。',
        // '你要是在我身边就好了，这句话并不是在怪你，而是在这瞬间我比平时要更想你。',
        // '下午三点适合见面，傍晚六点适合想念，夜晚十一点适合共眠。',
        // '你看，这么多人，这么大的世界，我遇到了你，你也遇到了我，真好。',
        // '世界上最动人的情话不是 “I love you”而是 “I have always been with you”（我一直在）。',
        '我希望睡前最后看到的是你。',
        '在这个快节奏的时代里，我想和你慢慢来。',
        // '春天浪漫，夏天丰富，秋天成熟，冬天庄严。路过，不要错过，这辈子都有命运，命运聚集着你我。',
        // '下雪的时候，想和你出去走一走，因为一不小心就牵了手，走着走着，就白了头。',
        // '一直忘了告诉你，我有多幸运，遇见的是你。我想有一天挽着你的手，去敬各位来宾的酒。',
        '结婚无需太伟大的爱情，彼此不讨厌已经够结婚资本了。',
        '我想要拍一部电影，男主是我，女主是你，电影叫往后余生。'
    ]

    let canvas,
        ctx,
        particles = [],
        quiver = true,
        text = texts[0],
        textIndex = 0,
        textSize = 40

    function draw() {
        ctx.clearRect(0, 0, CANVASWIDTH, CANVASHEIGHT)
        ctx.fillStyle = 'rgb(255, 255, 255)'
        ctx.textBaseline = 'middle'
        ctx.fontWeight = 'bold'
        ctx.font = textSize + 'px \'SimHei\', \'Avenir\', \'Helvetica Neue\', \'Arial\', \'sans-serif\''
        ctx.font = textSize + 'px \'SimHei\', \'Avenir\', \'Helvetica Neue\', \'Arial\', \'sans-serif\', subpixel-antialiased';
        ctx.fillText(text, (CANVASWIDTH - ctx.measureText(text).width) * 0.5, CANVASHEIGHT * 0.5)

        let imgData = ctx.getImageData(0, 0, CANVASWIDTH, CANVASHEIGHT)

        ctx.clearRect(0, 0, CANVASWIDTH, CANVASHEIGHT)

        for (let i = 0, l = particles.length; i < l; i++) {
            let p = particles[i]
            p.inText = false
        }
        particleText(imgData)

        window.requestAnimationFrame(draw)
    }

    function particleText(imgData) {
        // 点坐标获取
        var pxls = []
        for (var w = CANVASWIDTH; w > 0; w -= 3) {
            for (var h = 0; h < CANVASHEIGHT; h += 3) {
                var index = (w + h * (CANVASWIDTH)) * 4
                if (imgData.data[index] > 1) {
                    pxls.push([w, h])
                }
            }
        }

        var count = pxls.length
        var j = parseInt((particles.length - pxls.length) / 2, 10)
        j = j < 0 ? 0 : j

        for (var i = 0; i < pxls.length && j < particles.length; i++, j++) {
            try {
                var p = particles[j],
                    X,
                    Y

                if (quiver) {
                    X = (pxls[i - 1][0]) - (p.px + Math.random() * 10)
                    Y = (pxls[i - 1][1]) - (p.py + Math.random() * 10)
                } else {
                    X = (pxls[i - 1][0]) - p.px
                    Y = (pxls[i - 1][1]) - p.py
                }
                var T = Math.sqrt(X * X + Y * Y)
                var A = Math.atan2(Y, X)
                var C = Math.cos(A)
                var S = Math.sin(A)
                p.x = p.px + C * T * p.delta
                p.y = p.py + S * T * p.delta
                p.px = p.x
                p.py = p.y
                p.inText = true
                p.fadeIn()
                p.draw(ctx)
            } catch (e) {}
        }
        for (var i = 0; i < particles.length; i++) {
            var p = particles[i]
            if (!p.inText) {
                p.fadeOut()

                var X = p.mx - p.px
                var Y = p.my - p.py
                var T = Math.sqrt(X * X + Y * Y)
                var A = Math.atan2(Y, X)
                var C = Math.cos(A)
                var S = Math.sin(A)

                p.x = p.px + C * T * p.delta / 2
                p.y = p.py + S * T * p.delta / 2
                p.px = p.x
                p.py = p.y

                p.draw(ctx)
            }
        }
    }

    function setDimensions() {
        canvas.width = CANVASWIDTH
        canvas.height = CANVASHEIGHT
        canvas.style.position = 'absolute'
        canvas.style.left = '0px'
        canvas.style.top = '0px'
        canvas.style.bottom = '0px'
        canvas.style.right = '0px'
        canvas.style.marginTop = window.innerHeight * .15 + 'px'
    }

    function event() {
        document.addEventListener('click', function (e) {
            textIndex++
            if (textIndex >= texts.length) {
                textIndex--
                return
            }
            text = texts[textIndex]
            console.log(textIndex)
        }, false)

        document.addEventListener('touchstart', function (e) {
            textIndex++
            if (textIndex >= texts.length) {
                textIndex--
                return
            }
            text = texts[textIndex]
            console.log(textIndex)
        }, false)
    }

    function init() {
        canvas = document.getElementById(CANVASID)
        if (canvas === null || !canvas.getContext) {
            return
        }
        ctx = canvas.getContext('2d')
        setDimensions()
        event()

        for (var i = 0; i < PARTICLE_NUM; i++) {
            particles[i] = new Particle(canvas)
        }

        draw()
    }

    class Particle {
        constructor(canvas) {
            let spread = canvas.height
            // let size = Math.random() * 1.2
            // let size = Math.random() * (0.8 - 0.7) + 0.7;
            let size = 0.8
            // 速度
            this.delta = 0.06
            // 现在的位置
            this.x = 0
            this.y = 0
            // 上次的位置
            this.px = Math.random() * canvas.width
            this.py = (canvas.height * 0.5) + ((Math.random() - 0.5) * spread)
            // 记录点最初的位置
            this.mx = this.px
            this.my = this.py
            // 点的大小
            this.size = size
            // this.origSize = size
            // 是否用来显示字
            this.inText = false
            // 透明度相关
            this.opacity = 0
            this.fadeInRate = 0.005
            this.fadeOutRate = 0.03
            this.opacityTresh = 0.98
            this.fadingOut = true
            this.fadingIn = true
        }
        fadeIn() {
            this.fadingIn = this.opacity > this.opacityTresh ? false : true
            if (this.fadingIn) {
                this.opacity += this.fadeInRate
            } else {
                this.opacity = 1
            }
        }
        fadeOut() {
            this.fadingOut = this.opacity < 0 ? false : true
            if (this.fadingOut) {
                this.opacity -= this.fadeOutRate
                if (this.opacity < 0) {
                    this.opacity = 0
                }
            } else {
                this.opacity = 0
            }
        }
        draw(ctx) {
            ctx.fillStyle = 'rgba(226,225,142, ' + this.opacity + ')'
            ctx.beginPath()
            ctx.arc(this.x, this.y, this.size, 0, RADIUS, true)
            ctx.closePath()
            ctx.fill()
        }
    }

    // setTimeout(() => {
    init()
    // }, 4000);
    // mp3.play()
})(window)
