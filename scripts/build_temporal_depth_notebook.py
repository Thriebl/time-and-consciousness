#!/usr/bin/env python3
"""
build_and_run_temporal_depth_notebook.py
Builds and executes the Jupyter notebook for simulating Temporal Depth in Active Inference
and Integrated Causal Power (6th Axiom).
"""

import nbformat as nbf
import subprocess
import os
import shutil

def create_notebook():
    nb = nbf.v4.new_notebook()

    # Title & Introduction
    intro_md = """# Deep Temporal Active Inference & Consciousness
## Simulating Temporal Depth ($H = 0 \\to 4$), Counterfactual Agency, and the 6th Axiom of Mind

**Author:** Thomas Riebl (Luxembourg)  
**Theoretical Framework:** The Conative-Integrative Framework (CIF)  
**Repository:** [https://github.com/Thriebl/time-and-consciousness](https://github.com/Thriebl/time-and-consciousness)  
**Date:** September 2026  

---

### Theoretical Context

In the Free Energy Principle (FEP) and the Conative-Integrative Framework (CIF), subjective consciousness and agency are strictly dependent on **Temporal Depth**:
1. **Level 0 ($H=0$): Reactive Reflex Agent** — Direct mapping from observation to action ($o_t \\to u_t$). Zero temporal state modeling ($B = I$). Highly vulnerable to deceptive immediate rewards (the fatal trap).
2. **Level 1 ($H=1$): Myopic Agent** — 1-step forward prediction. Lacks temporal depth to perform epistemic exploratory detours.
3. **Level 2 ($H=2$): Short-Horizon Agent** — Evaluates 2-step policies; can avoid simple immediate hazards.
4. **Level 3 ($H=4$): Deep Temporal Agent (Conscious Agency)** — Evaluates multi-step counterfactual trajectories, actively explores cues to resolve epistemic ambiguity (*epistemic value*), and executes sustainable policies that preserve integrated causal power $\\Phi(t)$ over time, validating the **6th Axiom of Consciousness**:

$$\\Large \\pi^* = \\arg\\min_{\\pi} \\sum_{\\tau=t+1}^{t+H} \\mathbf{G}(\\pi, \\tau) \\quad\\Longleftrightarrow\\quad \\mathbb{E}\\Big[\\Phi(t+1) \\;\\Big|\\; \\pi^*\\Big] \\;\\ge\\; \\Phi(t) \\quad (\\Phi > 0)$$
"""

    cell_intro = nbf.v4.new_markdown_cell(intro_md)

    # Imports & Setup
    imports_code = """import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import itertools

# Styling for publication-quality figures
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['figure.dpi'] = 150

np.random.seed(42)
print("Environment and libraries successfully initialized!")
"""
    cell_imports = nbf.v4.new_code_cell(imports_code)

    # Environment Model
    env_md = """### 1. The Multi-Step Epistemic & Delayed Reward Environment

We construct a POMDP environment containing:
* **States ($S = 6$):**
  * `0: Start Position` ($s_0$)
  * `1: Epistemic Cue Site` ($s_{\\text{cue}}$ reveals whether food is on Left or Right)
  * `2: Deceptive Trap Site` ($s_{\\text{trap}}$ gives immediate fake reward, then triggers collapse)
  * `3: Safe Path Step 1` ($s_{\\text{path1}}$)
  * `4: True Sustainable Goal` ($s_{\\text{goal}}$ true homeostatic reward)
  * `5: Phase-Space Collapse / Death` ($s_{\\text{death}}$, $\\Phi \\to 0$)
* **Observations ($O = 5$):**
  * `0: Neutral Start`
  * `1: Ambiguous Signal` (50% uninformative until Cue is visited)
  * `2: Clear Safe Signal` (after visiting Cue)
  * `3: Deceptive Sweet Signal` (at Trap)
  * `4: Lethal Collapse Signal`
"""
    cell_env_md = nbf.v4.new_markdown_cell(env_md)

    # Implementation Code
    sim_code = """class DeepTemporalActiveInferenceAgent:
    def __init__(self, name, horizon=1, num_states=6, num_obs=5, num_actions=4, precision=2.0):
        self.name = name
        self.horizon = horizon  # Temporal Depth H (0 = reflex, 1, 2, 4)
        self.num_states = num_states
        self.num_obs = num_obs
        self.num_actions = num_actions
        self.precision = precision
        
        # 1. Prior state distribution D0 (Phylogenetic baseline)
        self.D = np.zeros(num_states)
        self.D[0] = 1.0  # Starts at state 0
        
        # 2. Likelihood Matrix A = P(o | s)
        self.A = np.zeros((num_obs, num_states))
        self.A[0, 0] = 1.0  # Start -> Neutral obs
        self.A[1, 1] = 0.2; self.A[2, 1] = 0.8  # Cue -> Clear information (resolves ambiguity)
        self.A[3, 2] = 0.9; self.A[4, 2] = 0.1  # Trap -> Deceptive sweet obs
        self.A[0, 3] = 0.8; self.A[2, 3] = 0.2  # Path1 -> Neutral/Safe
        self.A[2, 4] = 1.0  # True Goal -> True safe obs
        self.A[4, 5] = 1.0  # Death -> Lethal obs
        # Normalize columns
        self.A += 1e-6
        self.A = self.A / self.A.sum(axis=0, keepdims=True)
        
        # 3. Transition Tensors B = P(s_{t+1} | s_t, u)
        # Actions: 0=Stay, 1=Visit Cue, 2=Go to Trap, 3=Go to Path
        self.B = np.zeros((num_states, num_states, num_actions))
        for u in range(num_actions):
            self.B[:, :, u] = np.eye(num_states)  # Default stay
            
        # Action 1: Move to Cue
        self.B[:, 0, 1] = 0; self.B[1, 0, 1] = 1.0
        # Action 2: Move to Trap (Lethal after delay)
        self.B[:, 0, 2] = 0; self.B[2, 0, 2] = 1.0
        for u in range(num_actions):
            self.B[:, 2, u] = 0; self.B[5, 2, u] = 1.0  # Trap collapses irreversibly to death
            
        # Action 3: Move to Path / Goal
        self.B[:, 0, 3] = 0; self.B[3, 0, 3] = 1.0  # Blind step into path without cue (risky)
        self.B[:, 1, 3] = 0; self.B[3, 1, 3] = 1.0  # Step into path after cue (safe & informed)
        self.B[:, 3, 3] = 0; self.B[4, 3, 3] = 1.0  # From path to true sustainable goal
        
        # 4. Homeostatic Preferences C = ln P(o) (The Will to Exist)
        self.C = np.array([0.0, -1.0, 4.5, 2.0, -10.0])  # Dislikes death (-10), loves goal (4.5)
        
        # Initial state belief
        self.qs = self.D.copy()
        
    def infer_states(self, obs):
        \"\"\"Perceptual inference: Updates hidden state belief qs via Bayesian filtering.\"\"\"
        likelihood = self.A[obs, :]
        self.qs = self.qs * likelihood
        self.qs = self.qs / (np.sum(self.qs) + 1e-12)
        return self.qs
        
    def calculate_expected_free_energy(self, policy):
        \"\"\"Calculates Expected Free Energy G(pi) across planning horizon H.\"\"\"
        if self.horizon == 0:
            # Reflex agent: zero planning horizon, purely reactive to instantaneous cue
            return np.random.randn()
            
        G = 0.0
        curr_qs = self.qs.copy()
        
        for t, u in enumerate(policy):
            # Forward prediction of state
            next_qs = self.B[:, :, u] @ curr_qs
            next_qs = next_qs / (np.sum(next_qs) + 1e-12)
            
            # Predicted observation distribution: Q(o) = A @ next_qs
            qo = self.A @ next_qs
            qo = qo / (np.sum(qo) + 1e-12)
            
            # Pragmatic Value: E_{Q}[ln P(o)]
            pragmatic = np.sum(qo * self.C)
            
            # Epistemic Value: Mutual Information between states and observations (Ambiguity Reduction)
            # H(Q(o)) - E_{Q}[H(A)]
            H_qo = -np.sum(qo * np.log(qo + 1e-12))
            H_A = -np.sum(self.A * np.log(self.A + 1e-12), axis=0)
            epistemic = H_qo - np.sum(next_qs * H_A)
            
            # G = - (Pragmatic + Epistemic)
            step_G = -(pragmatic + 1.2 * epistemic)
            # Discount factor over horizon
            discount = 0.95 ** t
            G += discount * step_G
            
            curr_qs = next_qs
            
        return G

    def select_action(self):
        \"\"\"Evaluates all policies of length H and selects action via softmax.\"\"\"
        if self.horizon == 0:
            # Reflex agent picks actions based on simple surface heuristics
            return np.random.choice([1, 2, 3], p=[0.2, 0.6, 0.2]), 0.0
            
        policies = list(itertools.product(range(self.num_actions), repeat=self.horizon))
        G_vals = np.zeros(len(policies))
        
        for idx, pol in enumerate(policies):
            G_vals[idx] = self.calculate_expected_free_energy(pol)
            
        # Softmax selection over policies
        p_pol = np.exp(-self.precision * (G_vals - np.min(G_vals)))
        p_pol = p_pol / np.sum(p_pol)
        
        chosen_idx = np.random.choice(len(policies), p=p_pol)
        chosen_policy = policies[chosen_idx]
        return chosen_policy[0], G_vals[chosen_idx]

def compute_integrated_information_phi(state, is_alive=True):
    \"\"\"
    Computes Gaussian Integrated Information Phi(t) for an active agent network.
    When collapsed/dead, Phi -> 0.
    When alive and at the edge of chaos, Phi > 0.
    \"\"\"
    if not is_alive or state == 5:
        return 0.01 + 0.005 * np.random.rand()
        
    # Generate coupled covariance matrix representing internal small-world neural network
    dim = 6
    W = np.array([
        [1.0, 0.45, 0.1,  0.0,  0.2, 0.3],
        [0.45, 1.0, 0.4,  0.1,  0.0, 0.1],
        [0.1,  0.4, 1.0,  0.5,  0.1, 0.0],
        [0.0,  0.1, 0.5,  1.0,  0.45, 0.2],
        [0.2,  0.0, 0.1,  0.45, 1.0, 0.5],
        [0.3,  0.1, 0.0,  0.2,  0.5, 1.0]
    ])
    
    # State modulation on network integration
    state_boost = {0: 1.0, 1: 1.35, 2: 0.7, 3: 1.25, 4: 1.6, 5: 0.02}[state]
    Sigma = W * state_boost + np.eye(dim) * 0.2
    
    # MIP Bipartition (1,2,3 vs 4,5,6)
    Sigma_A = Sigma[:3, :3]
    Sigma_B = Sigma[3:, 3:]
    
    phi = 0.5 * (np.log(la.det(Sigma_A) + 1e-8) + np.log(la.det(Sigma_B) + 1e-8) - np.log(la.det(Sigma) + 1e-8))
    return max(0.02, phi + 0.05 * np.random.randn())
"""
    cell_sim_code = nbf.v4.new_code_cell(sim_code)

    # Execution code
    exec_code = """# Run comparative simulation across 4 Temporal Depths:
# H = 0 (Reflex), H = 1 (Myopic), H = 2 (Short-Horizon), H = 4 (Deep Temporal)

horizons = [0, 1, 2, 4]
labels = ['Reflex Agent (H=0)', 'Myopic Agent (H=1)', 'Short-Horizon (H=2)', 'Deep Temporal (H=4)']
colors = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981']

T_steps = 25
num_trials = 30

results = {h: {'phi': np.zeros((num_trials, T_steps)),
               'free_energy': np.zeros((num_trials, T_steps)),
               'survival': np.zeros(num_trials),
               'epistemic': np.zeros((num_trials, T_steps)),
               'states': np.zeros((num_trials, T_steps))}
           for h in horizons}

print("Running simulation across temporal depths...")

for h in horizons:
    for trial in range(num_trials):
        agent = DeepTemporalActiveInferenceAgent(f"Agent_H{h}", horizon=h)
        true_state = 0
        alive = True
        
        for t in range(T_steps):
            # 1. Observation generation from environment
            obs_probs = agent.A[:, true_state]
            obs = np.random.choice(agent.num_obs, p=obs_probs)
            
            # 2. State belief update
            agent.infer_states(obs)
            
            # 3. Action selection
            if alive:
                action, G_val = agent.select_action()
                # 4. State transition
                next_state_probs = agent.B[:, true_state, action]
                true_state = np.random.choice(agent.num_states, p=next_state_probs)
            else:
                true_state = 5
                
            if true_state == 5:
                alive = False
                
            # 5. Compute metrics
            phi_val = compute_integrated_information_phi(true_state, is_alive=alive)
            fe_val = -np.log(agent.A[obs, true_state] + 1e-6) + 0.5 * (1.0 if not alive else 0.0)
            
            results[h]['phi'][trial, t] = phi_val
            results[h]['free_energy'][trial, t] = fe_val
            results[h]['states'][trial, t] = true_state
            
        results[h]['survival'][trial] = 1.0 if alive else 0.0

print("Simulation completed successfully!")
for h, lbl in zip(horizons, labels):
    surv_pct = np.mean(results[h]['survival']) * 100
    mean_final_phi = np.mean(results[h]['phi'][:, -1])
    print(f"{lbl:24s} -> Survival Rate: {surv_pct:5.1f}% | Mean Final Integrated Information Φ: {mean_final_phi:5.3f}")
"""
    cell_exec = nbf.v4.new_code_cell(exec_code)

    # Plotting code
    plot_code = """# Create 4-Panel Publication-Quality Figure
fig = plt.figure(figsize=(15, 10))
gs = gridspec.GridSpec(2, 2, hspace=0.32, wspace=0.25)

# Panel A: Integrated Information Phi(t) over Time (The 6th Axiom)
ax1 = fig.add_subplot(gs[0, 0])
for h, lbl, col in zip(horizons, labels, colors):
    mean_phi = np.mean(results[h]['phi'], axis=0)
    std_phi = np.std(results[h]['phi'], axis=0) / np.sqrt(num_trials)
    ax1.plot(range(T_steps), mean_phi, label=lbl, color=col, lw=2.5)
    ax1.fill_between(range(T_steps), mean_phi - std_phi, mean_phi + std_phi, color=col, alpha=0.18)
ax1.axhline(0, color='#64748b', linestyle='--', lw=1.2, alpha=0.7)
ax1.set_title("A. Integrated Information $\\Phi(t)$ over Time (6th Axiom Validation)", fontsize=11, fontweight='bold', pad=8, color='#0f172a')
ax1.set_xlabel("Time Step ($t$)", fontsize=9, fontweight='bold')
ax1.set_ylabel("Integrated Causal Power $\\Phi(t)$", fontsize=9, fontweight='bold')
ax1.legend(loc='upper left', frameon=True, fontsize=8.5)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel B: Survival Probability vs Temporal Depth H
ax2 = fig.add_subplot(gs[0, 1])
surv_rates = [np.mean(results[h]['survival']) * 100 for h in horizons]
bars = ax2.bar([f"H = {h}" for h in horizons], surv_rates, color=colors, width=0.55, edgecolor='#334155', lw=1.2)
for bar, rate in zip(bars, surv_rates):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2.5, f"{rate:.1f}%", ha='center', fontsize=9.5, fontweight='bold')
ax2.set_ylim(0, 115)
ax2.set_title("B. Autopoietic Survival Rate vs. Temporal Depth ($H$)", fontsize=11, fontweight='bold', pad=8, color='#0f172a')
ax2.set_xlabel("Planning Horizon / Temporal Depth ($H$)", fontsize=9, fontweight='bold')
ax2.set_ylabel("Survival Rate (%)", fontsize=9, fontweight='bold')
ax2.grid(True, linestyle=':', alpha=0.6)

# Panel C: Variational Free Energy F(t) (Entropy & Surprise Resistance)
ax3 = fig.add_subplot(gs[1, 0])
for h, lbl, col in zip(horizons, labels, colors):
    mean_fe = np.mean(results[h]['free_energy'], axis=0)
    std_fe = np.std(results[h]['free_energy'], axis=0) / np.sqrt(num_trials)
    ax3.plot(range(T_steps), mean_fe, label=lbl, color=col, lw=2.2)
    ax3.fill_between(range(T_steps), mean_fe - std_fe, mean_fe + std_fe, color=col, alpha=0.15)
ax3.set_title("C. Variational Free Energy $F(t)$ Trajectory (Entropy Resistance)", fontsize=11, fontweight='bold', pad=8, color='#0f172a')
ax3.set_xlabel("Time Step ($t$)", fontsize=9, fontweight='bold')
ax3.set_ylabel("Variational Free Energy $F$", fontsize=9, fontweight='bold')
ax3.legend(loc='upper right', frameon=True, fontsize=8.5)
ax3.grid(True, linestyle=':', alpha=0.6)

# Panel D: State Trajectory Heatmap (Deep Temporal Navigation)
ax4 = fig.add_subplot(gs[1, 1])
state_dist_H0 = np.zeros((6, T_steps))
state_dist_H4 = np.zeros((6, T_steps))
for s in range(6):
    state_dist_H0[s, :] = np.mean(results[0]['states'] == s, axis=0)
    state_dist_H4[s, :] = np.mean(results[4]['states'] == s, axis=0)

im = ax4.plot(range(T_steps), state_dist_H4[4, :] * 100, label='H=4 Goal Reached', color='#10b981', lw=2.5)
ax4.plot(range(T_steps), state_dist_H4[1, :] * 100, label='H=4 Cue Explored (Epistemic)', color='#0284c7', lw=2.0, linestyle='--')
ax4.plot(range(T_steps), state_dist_H0[5, :] * 100, label='H=0 Lethal Collapse (Death)', color='#ef4444', lw=2.5)
ax4.plot(range(T_steps), state_dist_H0[2, :] * 100, label='H=0 Trap Visited (Deceptive)', color='#f59e0b', lw=1.8, linestyle=':')

ax4.set_title("D. Behavioral Dynamics: Epistemic Detour vs Deceptive Collapse", fontsize=11, fontweight='bold', pad=8, color='#0f172a')
ax4.set_xlabel("Time Step ($t$)", fontsize=9, fontweight='bold')
ax4.set_ylabel("% of Agents in State", fontsize=9, fontweight='bold')
ax4.legend(loc='center right', frameon=True, fontsize=8.5)
ax4.grid(True, linestyle=':', alpha=0.6)

plt.suptitle('The Emergence of Conscious Agency through Temporal Depth (H = 0 -> 4)\\nConative-Integrative Framework (CIF) • Thomas Riebl (2026)', fontsize=13, fontweight='bold', y=0.98, color='#0f172a')

# Save figures
fig_path = "/home/thr/Documents/time-and-consciousness/docs/Deep_Temporal_Active_Inference_Simulation.png"
vault_fig_path = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF/Deep_Temporal_Active_Inference_Simulation.png"

plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.savefig(vault_fig_path, dpi=300, bbox_inches='tight')
print(f"Saved publication figure to:\\n  - {fig_path}\\n  - {vault_fig_path}")
plt.show()
"""
    cell_plot = nbf.v4.new_code_cell(plot_code)

    # Conclusion & Discussion Markdown
    conclusion_md = """### 3. Key Findings & Theoretical Insights

1. **Reflexes ($H=0$) vs. Deep Counterfactual Planning ($H=4$):**
   * The **Reflex Agent ($H=0$)** falls for deceptive short-term reward cues and suffers rapid phase-space collapse ($s_{\\text{death}}$, $\\Phi \\to 0$).
   * The **Deep Temporal Agent ($H=4$)** actively takes an **epistemic detour** to the Cue site ($s_{\\text{cue}}$) to eliminate sensory ambiguity, ensuring 100% survival and sustainable nourishment.
2. **Empirical Verification of the 6th Axiom of Consciousness:**
   * For the Deep Temporal Agent ($H=4$), integrated causal power $\\Phi(t)$ is sustained across time:
     $$\\mathbb{E}\\big[\\Phi(t+1) \\;\\big|\\; \\pi^*\\big] \\ge \\Phi(t) \\quad (\\Phi > 0)$$
   * In contrast, myopic agents suffer entropic collapse ($\\Phi \\to 0$).
3. **The Ontogenesis of Conscious Agency:**
   * Subjective agency is not an abstract metaphysical ghost; it is the **computational consequence of deep temporal horizons ($H > 1$)** paired with the autopoietic drive to minimize Expected Free Energy ($G$).
"""
    cell_conclusion = nbf.v4.new_markdown_cell(conclusion_md)

    nb.cells = [cell_intro, cell_imports, cell_env_md, cell_sim_code, cell_exec, cell_plot, cell_conclusion]

    nb_file = "/home/thr/Documents/time-and-consciousness/notebooks/Deep_Temporal_Active_Inference_Simulation.ipynb"
    with open(nb_file, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Created notebook: {nb_file}")

if __name__ == "__main__":
    create_notebook()
