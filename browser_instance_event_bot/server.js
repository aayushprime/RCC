const express = require('express')
const app = express()
app.use(express.json());
const port = 3346


// Require puppeteer extra and puppeteer stealth
const puppeteer = require("puppeteer-extra");
const pluginStealth = require("puppeteer-extra-plugin-stealth");
const pluginRecaptcha = require("puppeteer-extra-plugin-recaptcha");
//require executablePath from puppeteer
const { executablePath } = require('puppeteer')

// Tell puppeteer to use puppeteer stealth
puppeteer.use(pluginStealth());
puppeteer.use(
    pluginRecaptcha({
        provider: { id: "2captcha", token: "5c2744d0debc0e0cfb3f176297bcbea4" },
        visualFeedback: true,
    })
);

let start_session = async (session_no) => {

    const browser = await puppeteer.launch({
        ignoreHTTPSErrors: true,
        headless: false,
        executablePath: executablePath(),
        userDataDir: `./sessions/session_${session_no.toString()}`,
        args: [
            `--window-size=600,1000`,
            "--window-position=000,000",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-web-security",
            "--disable-features=site-per-process",
        ],
    });

    // Get browser pages
    const [page] = await browser.pages();

    // Send page to your url
    await page.setCacheEnabled(false);
    await page.goto("https://stake.bet/settings/offers");
    await page.solveRecaptchas();

    return page;
}


let check_code = async (page, code) => {
    // Remove the page's default timeout function
    // await page.setDefaultNavigationTimeout(0);
    console.log("waiting for input field");
    let xptext =
        '//*[@id="scrollable"]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/section[2]/div[2]/div/div/label/div/div/input';
    await page.waitForXPath(xptext, { timeout: 5 * 60 * 1000 });
    await page.waitForTimeout(1000);
    const linkEx = await page.$x(xptext);
    if (linkEx.length > 0) {
        await linkEx[0].click();
    }
    await page.keyboard.type(code);
    let xpbtn =
        '//*[@id="scrollable"]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/section[2]/div[3]/button';
    console.log("waiting for button");
    await page.waitForXPath(xpbtn);
    await page.waitForTimeout(1000);

    let btn = await page.$x(xpbtn);
    if (btn.length > 0) {
        await btn[0].click();
    }
    let xpredeem = '//*[@id="svelte"]/div[1]/div[2]/div[2]/div/div/form/button';
    console.log("waiting for redeem button");
    await page.waitForXPath(xpredeem);
    await page.waitForTimeout(1000);

    btn = await page.$x(xpredeem);
    if (btn.length > 0) {
        await btn[0].click();
    }

    // wait for the captcha to load
    await page.waitForTimeout(3000);

    // Solve the captcha
    console.log("Solving captcha now!");
    const { captchas, solved, error } = await page.solveRecaptchas();
    console.log("CAPTCHAS:", captchas);
    if (solved) {
        console.log("Captcha solved!", solved);
    }
    if (error) {
        console.log("Error solving captcha: ", error);
    }

    console.log("Wait starts");
    await page.waitForTimeout(8000);
    console.log("Wait finish");
}




let MAX_SESSIONS = 2;
let fns = [];

(async () => {
    for (let i = 0; i < MAX_SESSIONS; i++) {
        fns.push(await start_session(i));
    }

})();



app.post('/', (req, res) => {
    try {
        code = req.body["code"];
        console.log(fns);
        res.send(`Working on it! ${code}`)
        for (var i = 0; i < fns.length; i++) {
            check_code(fns[i], code);
        }

    } catch (e) {
        console.log(e);
        res.send('Something went wrong!')
    }

})


app.listen(port, () => {
    console.log(`Listening on port ${port}`)
})