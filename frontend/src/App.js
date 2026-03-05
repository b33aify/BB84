import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [numBits, setNumBits] = useState(32);
  const [evePresent, setEvePresent] = useState(false);
  const [simulationData, setSimulationData] = useState(null);

  // 0: Idle, 1: Alice Prep, 2: Channel, 3: Bob Measure, 4: Sifting, 5: Result
  const [step, setStep] = useState(0);

  const runSimulation = async () => {
    try {
      // Reset animation state
      setStep(0);
      setSimulationData(null);

      const response = await axios.post('http://localhost:5000/simulate', {
        num_bits: numBits,
        eve_present: evePresent
      });

      // Start the animation sequence
      setSimulationData(response.data);
      triggerSequence();

    } catch (error) {
      console.error("Error connecting to backend:", error);
    }
  };

  const triggerSequence = () => {
    // Step 1: Alice prepares (Instant)
    setStep(1);

    // Step 2: Transmission (Start after 1s)
    setTimeout(() => setStep(2), 1000);

    // Step 3: Bob Measures (Start after 2.5s)
    setTimeout(() => setStep(3), 5500);

    // Step 4: Sifting (Start after 4s)
    setTimeout(() => setStep(4), 7000);

    // Step 5: Security Check / Final Result (Start after 5.5s)
    setTimeout(() => setStep(5), 8500);
  };

  return (
    <div className="App">
      <header className="header">
        <h1>BB84 Protocol</h1>
        <div className="controls">
          <label>
            Qubits:
            <input
              type="number"
              value={numBits}
              onChange={(e) => setNumBits(e.target.value)}
              min="5" max="50"
            />
          </label>
          <label className={`eve-toggle ${evePresent ? 'active' : ''}`}>
            <input
              type="checkbox"
              checked={evePresent}
              onChange={(e) => setEvePresent(e.target.checked)}
            />
            {evePresent ? 'Eve Active' : '🔒 Secure Mode'}
          </label>
          <button onClick={runSimulation} disabled={step > 0 && step < 5}>
            {step > 0 && step < 5 ? 'Running...' : 'Run Protocol'}
          </button>
        </div>
      </header>

      {simulationData && (
        <div className="simulation-container">

          {/* Lane 1: Alice */}
          <div className={`lane alice-lane ${step >= 1 ? 'visible' : ''}`}>
            <h3>Alice (Sender)</h3>
            <div className="bit-container">
              <div className="bit-row">
                <span className="label">Bits:</span>
                {simulationData.alice_bits.map((b, i) => (
                  <div key={i} className="bit-box pop-in" style={{animationDelay: `${i * 0.05}s`}}>{b}</div>
                ))}
              </div>
              <div className="bit-row">
                <span className="label">Bases:</span>
                {simulationData.alice_bases.map((b, i) => (
                  <div key={i} className="bit-box base-box pop-in" style={{animationDelay: `${i * 0.05 + 0.2}s`}}>
                    {b === '+' ? '+' : '×'}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Lane 2: The Channel */}
          <div className={`lane channel-lane ${step >= 2 ? 'visible' : ''}`}>

             {/* Moving Photons Animation */}
             {step === 2 && (
                <div className="photon-stream">
                  {simulationData.polarizations.map((p, i) => (
                    <div
                      key={i}
                      className={`flying-photon ${evePresent ? 'intercepted' : ''}`}
                      style={{
                        animationDelay: `${i * 0.1}s`,
                        left: `${(i / numBits) * 80 + 10}%`
                      }}
                    >
                      {p}
                    </div>
                  ))}
                </div>
             )}

            {/* NEW: Neutral Status Text. No spoilers! */}
            <div className="channel-status" style={{ color: '#4facfe' }}>
              {step >= 2 ? (
                <div>
                   <span style={{ fontSize: '1.2rem' }}>📡 Quantum Transmission Active...</span>
                   {evePresent && (
                     <div style={{ fontSize: '0.8rem', opacity: 0.7, marginTop: '5px' }}>
                     </div>
                   )}
                </div>
              ) : 'Waiting for transmission...'}
            </div>
          </div>

          {/* Lane 3: Bob */}
          <div className={`lane bob-lane ${step >= 3 ? 'visible' : ''}`}>
            <h3>Bob (Receiver)</h3>
            <div className="bit-row">
              <span className="label">Guess:</span>
              {simulationData.bob_bases.map((b, i) => (
                <div key={i} className="bit-box base-box pop-in" style={{animationDelay: `${i * 0.05}s`}}>
                  {b === '+' ? '+' : '×'}
                </div>
              ))}
            </div>
            <div className="bit-row">
              <span className="label">Result:</span>
              {simulationData.bob_results.map((b, i) => (
                <div key={i} className="bit-box pop-in" style={{animationDelay: `${i * 0.05 + 0.2}s`}}>{b}</div>
              ))}
            </div>
          </div>

          {/* Lane 4: Sifting & Security Check */}
          <div className={`lane sift-lane ${step >= 4 ? 'visible' : ''}`}>
            <h3>Sifting & Security Check</h3>

            {/* The Bits Comparison */}
            <div className="bit-row">
              <span className="label">Bases Match?</span>
              {simulationData.match_indices.map((match, i) => (
                <div
                  key={i}
                  className={`bit-box status-box ${match ? 'match-anim' : 'mismatch-anim'}`}
                  style={{animationDelay: `${i * 0.05}s`}}
                >
                  {match ? '✅' : '❌'}
                </div>
              ))}
            </div>

            {/* The Final Verdict Animation */}
            {step >= 5 && (
              <div className="final-key-section slide-up">

                <div className="security-report">
                  <p>Error Rate (QBER): <strong>{simulationData.qber ? simulationData.qber.toFixed(1) : 0}%</strong></p>
                  <p>Status: <span className={simulationData.key_secure ? 'safe-text' : 'danger-text'}>
                    {simulationData.key_secure ? 'SECURE' : 'COMPROMISED'}
                  </span></p>
                </div>

                {simulationData.key_secure ? (
                  /* SCENARIO A: SECURE */
                  <div>
                    <h4>Shared Secret Key:</h4>
                    <div className="key-display secure-key">
                      {simulationData.sifted_key.map((bit, i) => (
                         <span key={i} className="key-bit drop-in" style={{animationDelay: `${0.1 * i}s`}}>
                           {bit}
                         </span>
                      ))}
                    </div>
                  </div>
                ) : (
                  /* SCENARIO B: HACKED */
                  <div className="hacked-alert">
                    <h4>! EVE DETECTED !</h4>
                    <div className="key-display destroyed-key">
                      {simulationData.sifted_key.join('')}
                    </div>
                    <p style={{marginTop: '10px'}}>Key has been discarded.</p>
                  </div>
                )}
              </div>
            )}
          </div>

        </div>
      )}
    </div>
  );
}

export default App;