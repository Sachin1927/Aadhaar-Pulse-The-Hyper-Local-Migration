<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aadhaar-Pulse: Migration Observatory</title>
    <style>
        /* Base Variables and Reset */
        :root {
            --primary-blue: #0366d6;
            --text-main: #24292e;
            --text-muted: #586069;
            --bg-canvas: #ffffff;
            --bg-code: #f6f8fa;
            --border-light: #e1e4e8;
            --badge-green: #2ea44f;
            --badge-red: #cb2431;
            --badge-yellow: #d4a700;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-main);
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: var(--bg-canvas);
        }

        /* Typography */
        h1, h2, h3 {
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
            color: #1b1f23;
        }

        h1 {
            font-size: 2.2em;
            padding-bottom: 0.3em;
            border-bottom: 1px solid var(--border-light);
        }

        h2 {
            font-size: 1.65em;
            padding-bottom: 0.3em;
            border-bottom: 1px solid var(--border-light);
            margin-top: 40px;
        }

        h3 {
            font-size: 1.25em;
            color: #24292e;
        }

        p, li {
            font-size: 16px;
            margin-bottom: 16px;
        }

        /* Hero Image */
        .hero-container {
            text-align: center;
            margin: 30px 0;
        }

        .hero-img {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border: 1px solid var(--border-light);
        }

        .caption {
            font-style: italic;
            color: var(--text-muted);
            margin-top: 10px;
            font-size: 0.9em;
        }

        /* Badges */
        .badge-container {
            display: flex;
            gap: 8px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .badge img {
            height: 20px;
        }

        /* Code Blocks */
        pre {
            background-color: var(--bg-code);
            border-radius: 6px;
            padding: 16px;
            overflow: auto;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 85%;
            border: 1px solid var(--border-light);
            margin-bottom: 16px;
        }

        code {
            background-color: rgba(27,31,35,0.05);
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: monospace;
            font-size: 85%;
        }

        pre code {
            background-color: transparent;
            padding: 0;
            font-size: 100%;
        }

        /* Tables */
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
            display: block;
            overflow-x: auto;
        }

        th, td {
            padding: 10px 15px;
            border: 1px solid #dfe2e5;
            text-align: left;
        }

        th {
            background-color: #f6f8fa;
            font-weight: 600;
        }

        tr:nth-child(2n) {
            background-color: #f8f8f8;
        }

        /* Math Block (Simulated) */
        .math-block {
            background-color: #fff9c4; /* Light yellow for visibility */
            border-left: 5px solid #fbc02d;
            padding: 15px;
            margin: 20px 0;
            font-family: "Times New Roman", serif;
            font-size: 1.3em;
            text-align: center;
            border-radius: 4px;
        }

        /* Custom Highlights */
        .highlight-box {
            background-color: #f1f8ff;
            border: 1px solid #c8e1ff;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 16px;
        }

        blockquote {
            color: var(--text-muted);
            border-left: 4px solid #dfe2e5;
            padding: 0 1em;
            margin-left: 0;
        }

        /* Footer */
        footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid var(--border-light);
            text-align: center;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

    <header>
        <h1>🇮🇳 Aadhaar-Pulse: Inter-District Migration Observatory</h1>
        <p style="font-size: 1.1em; color: var(--text-muted);">
            <em>Hyper-local Decision Support System (DSS) for Administrative Resource Allocation</em>
        </p>

        <div class="badge-container">
            <a href="https://www.python.org/downloads/" class="badge">
                <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+">
            </a>
            <a href="https://streamlit.io/" class="badge">
                <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" alt="Streamlit">
            </a>
            <a href="https://pola.rs/" class="badge">
                <img src="https://img.shields.io/badge/Polars-⚡_Fast_Engine-yellow" alt="Polars Engine">
            </a>
            <a href="https://opensource.org/licenses/MIT" class="badge">
                <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
            </a>
        </div>
    </header>

    <main>
        <div class="hero-container">
            <img src="aadhaar_pulse_dashboard.png" alt="Aadhaar-Pulse Dashboard Overview" class="hero-img">
            <p class="caption">Figure 1: Full Dashboard View demonstrating District-Level Drilldown, Descriptive Analytics, and AI-Driven Prescriptive Forecasting.</p>
        </div>

        <section id="abstract">
            <h2>📋 Abstract</h2>
            <p><strong>Aadhaar-Pulse</strong> is a privacy-preserving data analytics platform designed for the UIDAI Hackathon. It addresses the critical information gap regarding real-time internal migration in India. By leveraging administrative footprints—specifically comparing natural demographic growth against high-frequency address updates—the system calculates a <strong>Migrant Load Index (MLI)</strong>. This enables District Administrators to proactively identify infrastructure stress points and optimize resource allocation (water, ration, housing) before crises occur.</p>
        </section>

        <section id="problem">
            <h2>🚨 The Problem Statement</h2>
            <p>Census data, collected decadally, is insufficient for tracking modern, dynamic migration patterns. This data lag creates a "blind spot" for administrators, leading to:</p>
            <ol>
                <li><strong>Reactive Governance:</strong> Resources are allocated only after shortages (e.g., water scarcity in industrial hubs) become critical.</li>
                <li><strong>Infrastructure Strain:</strong> Unexpected population surges overwhelm local services in specific districts.</li>
                <li><strong>Privacy Dilemma:</strong> Tracking individual movement to understand migration flow violates the Aadhaar Act's privacy mandates.</li>
            </ol>
        </section>

        <section id="solution">
            <h2>💡 The Solution</h2>
            <p>Aadhaar-Pulse utilizes anonymized aggregate data to create live proxy indicators for migration pressure. It shifts the focus from <em>"Where did they come from?"</em> (which is privacy-intrusive) to <strong><em>"Where are they going, and what is the impact?"</em> (which is actionable governance).</strong></p>
            
            <div class="highlight-box">
                <h3>Key Capabilities:</h3>
                <ul>
                    <li><strong>Descriptive Analytics:</strong> Real-time assessment of current migration pressure at both State and District levels.</li>
                    <li><strong>Prescriptive Analytics:</strong> AI-driven actionable recommendations based on severity and forecasted trends.</li>
                    <li><strong>Context-Aware Visualization:</strong> Dynamic charts that adapt based on the user's drill-down level (e.g., State Heatmaps vs. District Comparative Bell Curves).</li>
                </ul>
            </div>
        </section>

        <section id="methodology">
            <h2>⚙️ Methodology: The Migrant Load Index (MLI)</h2>
            <p>We quantify infrastructure pressure using a custom metric, the <strong>Migrant Load Index (MLI)</strong>. It is a ratio of administrative inward flow relative to organic natural growth.</p>

            <div class="math-block">
                MLI = ( Inward Administrative Flow ) / ( Natural Growth + 1 )
            </div>

            <ul>
                <li><strong>Numerator (Inflow Signal):</strong> Sum of demographic updates across age brackets (proxies for active migration).</li>
                <li><strong>Denominator (Base Signal):</strong> New child enrolments (aged 0-5), representing natural organic population growth.</li>
                <li><strong>Noise Filtering:</strong> A magnitude threshold applies; districts with insignificant absolute update volumes are filtered to prevent statistical skew.</li>
            </ul>

            <table>
                <thead>
                    <tr>
                        <th>MLI Score</th>
                        <th>Risk Status</th>
                        <th>Interpretation</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>&lt; 1.5</strong></td>
                        <td>🟢 STABLE</td>
                        <td>Organic growth. Maintain standard monitoring.</td>
                    </tr>
                    <tr>
                        <td><strong>1.5 - 3.0</strong></td>
                        <td>🟠 WARNING</td>
                        <td>Elevated turnover. Monitor housing and labor sectors.</td>
                    </tr>
                    <tr>
                        <td><strong>&gt; 3.0</strong></td>
                        <td>🔴 CRITICAL</td>
                        <td>Influx significantly exceeds natural base. Immediate intervention required.</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <section id="tech-stack">
            <h2>🛠️ Technical Architecture & Stack</h2>
            <p>The application is built for performance and scalability, utilizing modern data engineering tools.</p>

            <table>
                <thead>
                    <tr>
                        <th>Component</th>
                        <th>Technology</th>
                        <th>Key Rationale</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Data Processing Engine</strong></td>
                        <td><strong>Polars (Rust)</strong></td>
                        <td>Chosen over Pandas for its blazingly fast, multi-threaded performance on large datasets and lazy evaluation capabilities.</td>
                    </tr>
                    <tr>
                        <td><strong>Frontend Interface</strong></td>
                        <td><strong>Streamlit</strong></td>
                        <td>Enables rapid development of interactive, highly customized web applications with Python.</td>
                    </tr>
                    <tr>
                        <td><strong>Visualization Layer</strong></td>
                        <td><strong>Plotly Express / FF</strong></td>
                        <td>Provides interactive, publication-quality charts (Heatmaps, Bell Curves, Line Charts).</td>
                    </tr>
                    <tr>
                        <td><strong>Predictive Modeling</strong></td>
                        <td><strong>NumPy / SciPy</strong></td>
                        <td>Used for statistical analysis and time-series linear growth projections.</td>
                    </tr>
                    <tr>
                        <td><strong>Data Ingestion</strong></td>
                        <td><strong>Recursive Globbing</strong></td>
                        <td>Robust file handling that automatically scans complex, nested directory structures for partitioned data files.</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <section id="installation">
            <h2>🚀 Installation & Setup Guide</h2>
            <p>Follow these steps to deploy the application locally.</p>

            <h3>Prerequisites</h3>
            <ul><li>Python 3.9 or higher</li></ul>

            <h3>Step 1: Clone Repository</h3>
            <pre><code>git clone https://github.com/YOUR_USERNAME/aadhaar-pulse.git
cd aadhaar-pulse</code></pre>

            <h3>Step 2: Install Dependencies</h3>
            <p>It is recommended to use a virtual environment.</p>
            <pre><code>pip install -r requirements.txt</code></pre>

            <h3>Step 3: Data Configuration</h3>
            <p>Ensure the raw data folders are present in the project root directory. The system will automatically scan them recursively.</p>
            <pre><code>/api_data_aadhaar_enrolment/
/api_data_aadhaar_demographic/</code></pre>

            <h3>Step 4: Launch Application</h3>
            <pre><code>streamlit run app.py</code></pre>
            <p>The dashboard will open automatically in your default web browser at <code>http://localhost:8501</code>.</p>
        </section>

        <section id="roadmap">
            <h2>🔮 Future Roadmap</h2>
            <ul>
                <li><strong>Geospatial Integration:</strong> Mapping ward-level data onto GIS layers using Mapbox for precise hotspot localization.</li>
                <li><strong>GenAI Reporting:</strong> Integrating LLMs (e.g., Llama-2) to auto-generate comprehensive PDF policy briefs for ministerial review.</li>
                <li><strong>Inter-Departmental API:</strong> Exposing live MLI scores via REST endpoints for integration with PDS (Ration) and Urban Planning systems.</li>
            </ul>
        </section>

    </main>

    <footer>
        <p>👨‍💻 <strong>Developed for UIDAI Hackathon 2026</strong></p>
    </footer>

</body>
</html>
