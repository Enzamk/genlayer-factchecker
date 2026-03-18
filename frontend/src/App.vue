<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { createClient } from 'genlayer-js'
import { studionet } from 'genlayer-js/chains'
import { privateKeyToAccount } from 'viem/accounts'

const privateKey = import.meta.env.VITE_PRIVATE_KEY as `0x${string}`
const account = privateKeyToAccount(privateKey)
const client = createClient({ chain: studionet, account })
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS as `0x${string}`

const checks = ref<any[]>([])
const claim = ref('')
const loading = ref(false)
const checking = ref(false)
const status = ref('')

async function fetchChecks() {
  loading.value = true
  try {
    const result = await client.readContract({
      address: contractAddress,
      functionName: 'get_checks',
      args: [],
      account: account.address,
    })
    checks.value = (result as any[]).reverse()
  } catch (e: any) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitClaim() {
  if (!claim.value.trim()) return
  checking.value = true
  status.value = 'Sending to AI validators...'
  try {
    await client.writeContract({
      address: contractAddress,
      functionName: 'check_fact',
      args: [claim.value.trim()],
    })
    status.value = 'Validators checking... please wait 30s then refresh'
    claim.value = ''
    setTimeout(() => { fetchChecks(); status.value = '' }, 30000)
  } catch (e: any) {
    status.value = 'Error: ' + e.message
  } finally {
    checking.value = false
  }
}

onMounted(fetchChecks)
</script>

<template>
  <div class="app">
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>
    <div class="container">
      <header class="header">
        <div class="logo">
          <div class="logo-icon">
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
              <polygon points="13,2 24,7 24,19 13,24 2,19 2,7" stroke="#00f5c4" stroke-width="1.5" fill="none"/>
              <path d="M8 13h10M13 8v10" stroke="#00f5c4" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <div>
            <h1 class="title">AI Fact Checker</h1>
            <span class="subtitle">Powered by GenLayer · 5 AI Validators</span>
          </div>
        </div>
        <div class="network-badge"><span class="dot"></span>studionet</div>
      </header>

      <div class="input-card">
        <div class="card-label">SUBMIT A CLAIM TO VERIFY</div>
        <div class="examples">
          <span class="ex-label">Try:</span>
          <button class="ex-btn" @click="claim = 'The Earth is round'">The Earth is round</button>
          <button class="ex-btn" @click="claim = 'Bitcoin was created in 2009'">Bitcoin was created in 2009</button>
          <button class="ex-btn" @click="claim = 'Python is older than JavaScript'">Python is older than JavaScript</button>
        </div>
        <div class="input-row">
          <input v-model="claim" placeholder="Enter any claim to fact-check..." class="input" :disabled="checking" @keyup.enter="submitClaim"/>
          <button class="submit-btn" @click="submitClaim" :disabled="checking || !claim.trim()">
            <span v-if="checking" class="spinner"></span>
            <span v-else>Check Fact</span>
          </button>
        </div>
        <div v-if="status" class="status-msg"><span class="status-dot"></span>{{ status }}</div>
      </div>

      <div class="results-card">
        <div class="results-header">
          <div class="card-label">FACT CHECK RESULTS</div>
          <button class="refresh-btn" @click="fetchChecks" :disabled="loading">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
            Refresh
          </button>
        </div>
        <div v-if="loading" class="loading-state"><div class="loading-dots"><span></span><span></span><span></span></div></div>
        <div v-else-if="checks.length === 0" class="empty-state">No fact checks yet. Submit a claim above!</div>
        <div v-else class="checks-list">
          <div v-for="(check, i) in checks" :key="i" class="check-item" :class="check.verdict === 'TRUE' ? 'true' : 'false'">
            <div class="verdict-badge" :class="check.verdict === 'TRUE' ? 'badge-true' : 'badge-false'">
              <span v-if="check.verdict === 'TRUE'">✓ TRUE</span>
              <span v-else>✕ FALSE</span>
            </div>
            <div class="check-body">
              <div class="check-claim">"{{ check.claim }}"</div>
              <div class="check-reason">{{ check.reason }}</div>
            </div>
          </div>
        </div>
      </div>

      <footer class="footer">
        <span>{{ contractAddress.slice(0,6) }}...{{ contractAddress.slice(-4) }}</span>
        <span class="sep">·</span><span>5 validator consensus</span>
        <span class="sep">·</span><span>GenLayer studionet</span>
      </footer>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--neon:#00f5c4;--neon-dim:rgba(0,245,196,0.12);--neon-glow:rgba(0,245,196,0.35);--bg:#050a0e;--surface:rgba(255,255,255,0.03);--border:rgba(0,245,196,0.15);--text:#e2e8f0;--text-dim:rgba(226,232,240,0.45);--true:rgba(0,245,196,0.1);--true-border:rgba(0,245,196,0.3);--false:rgba(255,77,109,0.08);--false-border:rgba(255,77,109,0.25)}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;min-height:100vh}
.app{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;position:relative;overflow:hidden}
.bg-grid{position:fixed;inset:0;background-image:linear-gradient(rgba(0,245,196,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,245,196,0.04) 1px,transparent 1px);background-size:48px 48px;pointer-events:none}
.bg-glow{position:fixed;width:500px;height:500px;background:radial-gradient(circle,rgba(0,245,196,0.07) 0%,transparent 70%);top:-150px;right:-150px;pointer-events:none}
.container{width:100%;max-width:580px;display:flex;flex-direction:column;gap:12px;position:relative;z-index:1}
.header{display:flex;align-items:center;justify-content:space-between;padding:18px 22px;background:var(--surface);border:1px solid var(--border);border-radius:16px;backdrop-filter:blur(20px)}
.logo{display:flex;align-items:center;gap:12px}
.logo-icon{width:46px;height:46px;background:var(--neon-dim);border:1px solid var(--border);border-radius:12px;display:flex;align-items:center;justify-content:center}
.title{font-family:'Space Mono',monospace;font-size:18px;font-weight:700;color:var(--neon);line-height:1}
.subtitle{font-size:11px;color:var(--text-dim)}
.network-badge{display:flex;align-items:center;gap:6px;padding:5px 12px;background:var(--neon-dim);border:1px solid var(--border);border-radius:20px;font-family:'Space Mono',monospace;font-size:11px;color:var(--neon)}
.dot{width:6px;height:6px;background:var(--neon);border-radius:50%;animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
.input-card,.results-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:20px 22px;backdrop-filter:blur(20px)}
.card-label{font-family:'Space Mono',monospace;font-size:10px;color:var(--text-dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:12px}
.examples{display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:14px}
.ex-label{font-size:12px;color:var(--text-dim)}
.ex-btn{background:rgba(0,245,196,0.06);border:1px solid var(--border);border-radius:20px;padding:4px 10px;font-size:11px;color:var(--neon);cursor:pointer;transition:all 0.2s;font-family:'DM Sans',sans-serif}
.ex-btn:hover{background:var(--neon-dim);border-color:rgba(0,245,196,0.4)}
.input-row{display:flex;gap:10px}
.input{flex:1;background:rgba(0,0,0,0.3);border:1px solid var(--border);border-radius:10px;padding:12px 14px;color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;outline:none;transition:border-color 0.2s,box-shadow 0.2s}
.input::placeholder{color:var(--text-dim)}
.input:focus{border-color:var(--neon);box-shadow:0 0 0 3px var(--neon-dim)}
.input:disabled{opacity:0.5}
.submit-btn{display:flex;align-items:center;justify-content:center;padding:12px 20px;background:var(--neon);border:none;border-radius:10px;color:#050a0e;font-family:'DM Sans',sans-serif;font-size:14px;font-weight:700;cursor:pointer;transition:all 0.2s;min-width:120px}
.submit-btn:hover:not(:disabled){background:#00ffd0;box-shadow:0 0 20px var(--neon-glow);transform:translateY(-1px)}
.submit-btn:disabled{opacity:0.4;cursor:not-allowed;transform:none}
.status-msg{display:flex;align-items:center;gap:8px;margin-top:12px;font-size:13px;color:var(--neon);padding:10px 14px;background:var(--neon-dim);border:1px solid var(--border);border-radius:8px}
.status-dot{width:8px;height:8px;background:var(--neon);border-radius:50%;animation:pulse 1s ease-in-out infinite;flex-shrink:0}
.results-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.refresh-btn{display:flex;align-items:center;gap:5px;background:none;border:none;cursor:pointer;color:var(--text-dim);font-size:12px;font-family:'DM Sans',sans-serif;padding:4px 8px;border-radius:6px;transition:all 0.2s}
.refresh-btn:hover:not(:disabled){color:var(--neon);background:var(--neon-dim)}
.loading-state{display:flex;justify-content:center;padding:24px}
.loading-dots{display:flex;gap:6px;align-items:center}
.loading-dots span{width:8px;height:8px;background:var(--neon);border-radius:50%;animation:bounce 1.2s ease-in-out infinite}
.loading-dots span:nth-child(2){animation-delay:0.2s}
.loading-dots span:nth-child(3){animation-delay:0.4s}
@keyframes bounce{0%,80%,100%{transform:scale(0.6);opacity:0.4}40%{transform:scale(1);opacity:1}}
.empty-state{text-align:center;padding:32px;color:var(--text-dim);font-size:14px}
.checks-list{display:flex;flex-direction:column;gap:10px}
.check-item{display:flex;gap:14px;align-items:flex-start;padding:14px;border-radius:10px;border:1px solid}
.check-item.true{background:var(--true);border-color:var(--true-border)}
.check-item.false{background:var(--false);border-color:var(--false-border)}
.verdict-badge{flex-shrink:0;padding:4px 10px;border-radius:20px;font-family:'Space Mono',monospace;font-size:11px;font-weight:700;white-space:nowrap}
.badge-true{background:rgba(0,245,196,0.15);color:var(--neon)}
.badge-false{background:rgba(255,77,109,0.15);color:#ff4d6d}
.check-body{flex:1}
.check-claim{font-size:14px;font-weight:500;color:var(--text);margin-bottom:4px}
.check-reason{font-size:12px;color:var(--text-dim);line-height:1.5}
.spinner{width:16px;height:16px;border:2px solid rgba(5,10,14,0.3);border-top-color:#050a0e;border-radius:50%;animation:spin 0.7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.footer{display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;font-size:11px;color:var(--text-dim)}
.sep{color:var(--border)}
</style>
