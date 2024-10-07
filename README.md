<h1 id="data-structures-in-the-ukssdc-module">Data structures in the <code>ukssdc</code> module.</h1>
<p>There are a few data structures used throughout the <code>swifttools.ukssdc</code> module, for which this page is
the reference.</p>
<p>These are:</p>
<ul>
<li><a href="#the-light-curve-dict">Light curve <code>dict</code>s</a></li>
<li><a href="#the-spectrum-dict">Spectrum <code>dict</code>s</a></li>
<li><a href="#the-burst-analyser-dict">Burst Analyser <code>dict</code>s</a></li>
</ul>
<p>The first two appear in quite a few places, the last one is only present for GRBs.
All three are explained and demonstrated below in some detail. In each case I first give a short explanation of
the structure, then an example, and then a detailed walkthrough the contents&dagger;. My hope is that you can glance over
the introduction and this will be enough that these make sense when you encounter them in the main
documentation. The full details are there for only when you really need them. But please do read them before contacting
me for help&hellip;</p>
<p>(&dagger; For the burst analyser <code>dict</code> I do not give a walkthrough. Since that data structure is only used
for GRBs the walkthrough appears on the <a href="data/GRB.md#burst-analyser"><code>swifttools.ukssdc.data.GRB</code> page</a>).</p>
<h2 id="the-light-curve-dict">The light curve dict</h2>
<p>Light curves are all stored in a <code>dict</code> following a specific structure, and referred to throughout
this documentation as a &quot;light curve <code>dict</code>&quot;. This, as the name suggests, is a Python <code>dict</code> and
it contains the following keys:</p>
<ul>
<li>'Datasets' - This is a list of all of the light curves downloaded.</li>
<li>'Binning' (optional) - The method used to bin the data.</li>
<li>'TimeFormat' (optional) - The time format used for the time axis.</li>
<li>'T0' (optional) - The zeropoint of the light curve, in Swift MET (see below).</li>
<li>'URLs' (optional) - A <code>dict</code> giving, for each light curve in <code>Datasets</code>, the URL to the light curve file.</li>
</ul>
<p>There will also be a key for each entry in <code>Datasets</code>, the value of which is the actual light curve, in the form of a pandas <code>DataFrame</code>.
As you can see, not all of these keys need to exist for the object to be a light curve <code>dict</code>, only the  'Datasets'
key, and a key for each entry in 'Datasets' are guaranteed to exist.</p>
<p>This structure is probably best demonstrated, and the values explained, with an example:</p>
<pre><code class="language-python">{
  'Datasets': ['WT', 'WT_incbad', 'PC', 'PC_incbad', 'PCUL', 'PCUL_incbad', 'PCHard', 'PCSoft', 'PCHR'],
  'Binning': 'Counts',
  'TimeFormat': 'MET',
  'T0': 672786064,
  'URLs': {'WT_incbad':'https://www.swift.ac.uk/xrt_curves/01104343/WTCURVE.qdp', ...}
  'WT_incbad': ...,
  'PC_incbad': ...,
  'PCUL_incbad': ...,
  ...
}</code></pre>
<p>In the above I have suppressed some contents for readability. Now let's go through these
in turn and see what they mean,</p>
<h3 id="datasets">Datasets</h3>
<pre><code class="language-python">  'Datasets': ['WT', 'WT_incbad', 'PC', 'PC_incbad', 'PCUL_incbad', 'PCHard', 'PCSoft', 'PCHR'],</code></pre>
<p>The 'Datasets' key is just a list of all the light curves contained in the set; the above is not exhaustive,
just intended to give a reasonable range. The format of the name is as follows:</p>
<p><code>$mode$what$nosys$incbad</code></p>
<p>Where the elements are:</p>
<dl>
<dt>$mode</dt>
<dd>The XRT mode, &quot;WT&quot; or &quot;PC&quot;.</dd>
<dt>$what</dt>
<dd>The type of light curve. If blank, a normal light curve; &quot;UL&quot; indicates it contains upper limits, and
&quot;Hard&quot;, &quot;Soft&quot;, &quot;HR&quot; indicate that the data are the hard band, soft band or hardness ratio time series respectively.</dd>
<dt>$nosys</dt>
<dd>Either blank or &quot;_nosys&quot;; the latter indicating that the WT-mode systematic errors have been removed.</dd>
<dt>$incbad</dt>
<dd>Either blank or &quot;_incbad&quot;; the latter indicating that the datapoints where the XRT centroid could not be verified
have been excluded.</dd>
</dl>
<p>So, for example, the dataset &quot;WT&quot; is the WT-mode light curve, with systematics and without the unreliable datapoints.
&quot;PCUL_incbad&quot; is the PC-mode upper limits, including potentially unreliable datapoints.</p>
<p>For an explanation of the systematics and unreliable datapoints, please see the <a href="https://www.swift.ac.uk/user_objects/lc_docs.php#systematics">the light curve
documentation</a>.</p>
<h3 id="binning">Binning</h3>
<pre><code class="language-python">  'Binning': 'Counts',</code></pre>
<p>The 'Binning' entry is a single string indicating how the light curve was binned. This will be one of the following:</p>
<dl>
<dt>Counts</dt>
<dd>Binned based on the counts per bin (&quot;GRB-style&quot;)</dd>
<dt>Time</dt>
<dd>Bins with fixed durations</dd>
<dt>Observation</dt>
<dd>One bin for each Swift obsid.</dd>
<dt>Snapshot</dt>
<dd>One bin for each snapshot (continuous pointing with Swift).</dd>
<dt>Unknown</dt>
<dd>For some reason the binning method was not recorded.</dd>
</dl>
<h3 id="timeformat">TimeFormat</h3>
<pre><code class="language-python">  'TimeFormat': 'MET',</code></pre>
<p>The 'TimeFormat' entry tells you what the value in the Time columns actually mean. These can be</p>
<dl>
<dt>MJD</dt>
<dd>Modified Julian Date (UTC)</dd>
<dt>TDB</dt>
<dd>Barycentric dynamical time.</dd>
<dt>MET</dt>
<dd>Swift Mission Elapsed Time. This is a value in seconds, either since the Swift reference time (2001 Jan 01 at 00:00:00 UTC),
or in seconds since the value in the 'T0' entry.</dd>
</dl>
<p><a id='metwarn'></a>
Note that MET values are determined by the spacecraft onboard clock; to convert this to a universal time system such as
a UT calendar date, MJD etc, requires knowledge of the spacecraft clock drift and the leap second history. We recommend
using the <code>swifttime</code> tool included in <code>HEASoft</code>, which fully corrects for these effects.</p>
<h3 id="t0">T0</h3>
<pre><code class="language-python">  'T0': 672786064,</code></pre>
<p>The 'T0' entry gives the zeropoint used for the light curve. It is in Swift Mission Elapsed Time, which is seconds
since 2001 Jan 01 at 00:00:00 UTC (as counted by the spacecraft onboard clock). This is really only of interest if the 'TimeFormat' is 'MET'
since the other values are absolute anyway.</p>
<p>Please do note the warning above about converting MET to absolute time systems.</p>
<h3 id="urls">URLs</h3>
<pre><code class="language-python">  'URLs' : {

    'WT': 'https://www.swift.ac.uk/xrt_curves/01104343/WTCURVE.qdp',
    'WT_incbad': 'https://www.swift.ac.uk/xrt_curves/01104343/WTCURVE.qdp',
    'PC': 'https://www.swift.ac.uk/xrt_curves/01104343/PCCURVE.qdp',
    'PC_incbad': 'https://www.swift.ac.uk/xrt_curves/01104343/PCCURVE_incbad.qdp',
    'PCUL_incbad': 'https://www.swift.ac.uk/xrt_curves/01104343/PCUL_incbad.qdp',
    'PCHard': 'https://www.swift.ac.uk/xrt_curves/01104343/PCHR.qdp',
    'PCSoft': 'https://www.swift.ac.uk/xrt_curves/01104343/PCHR.qdp',
    'PCHR': 'https://www.swift.ac.uk/xrt_curves/01104343/PCHR.qdp',
  }</code></pre>
<p>The 'URLs' entry is a <code>dict</code> with a key for each of the datasets downloaded (and given in 'Datasets'). This points to the
raw light curve data file from which the <code>DataFrame</code>s were built, so you can readily get at the original files yourself if you wish.</p>
<h3 id="the-actual-light-curves">The actual light curves</h3>
<p>And lastly we come to what you've been waiting patiently for: the actual light curves.</p>
<p>These are simply <code>pandas DataFrame</code> objects containing the light curve data. The columns depends on the light curve type,
and some examples (with the rows truncated) are given below. If you want full details of what each row means,
you'll need to see <a href="https://www.swift.ac.uk/user_objects/lc_docs.php#format">the light curve documentation</a>.</p>
<p>First, here's an example of a normal light curve (here, 'PC_incbad'):</p>
<div style="width: 95%; max-height: 200px; overflow: scroll;"><style scoped>    .dataframe tbody tr th:only-of-type {        vertical-align: middle;    }    .dataframe tbody tr th {        vertical-align: top;    }    .dataframe thead th {        text-align: right;    }</style><table border="1" class="dataframe">  <thead>    <tr style="text-align: right;"><th></th><th>Time</th><th>TimePos</th><th>TimeNeg</th><th>Rate</th><th>RatePos</th><th>RateNeg</th><th>FracExp</th><th>BGrate</th><th>BGerr</th><th>CorrFact</th><th>CtsInSrc</th><th>BGInSrc</th><th>Exposure</th><th>Sigma</th><th>SNR</th></tr>  </thead>  <tbody><tr><th>0</th><td>231.329</td><td>9.456</td><td>-10.603</td><td>2.492634</td><td>0.547598</td><td>-0.547598</td><td>1.000000</td><td>0.006904</td><td>0.003088</td><td>2.396688</td><td>21.0</td><td>0.138491</td><td>20.058508</td><td>336.828549</td><td>4.551939</td></tr><tr><th>1</th><td>254.712</td><td>8.638</td><td>-13.928</td><td>2.458382</td><td>0.502403</td><td>-0.502403</td><td>1.000000</td><td>0.001227</td><td>0.001227</td><td>2.314148</td><td>24.0</td><td>0.027698</td><td>22.565840</td><td>865.481752</td><td>4.893247</td></tr><tr><th>2</th><td>272.685</td><td>10.724</td><td>-9.335</td><td>2.265870</td><td>0.510246</td><td>-0.510246</td><td>1.000000</td><td>0.006904</td><td>0.003088</td><td>2.288348</td><td>20.0</td><td>0.138491</td><td>20.058540</td><td>320.682615</td><td>4.440743</td>    </tr>  <tr><td colspan="13" style="text-align: left;">…</td></tr>  </tbody></table></div>
<p>An upper limit is similar, except that the &quot;Rate&quot; column is replaced with &quot;UpperLimit&quot;:</p>
<div style="width: 95%; max-height: 200px; overflow: scroll;"><style scoped>    .dataframe tbody tr th:only-of-type {        vertical-align: middle;    }    .dataframe tbody tr th {        vertical-align: top;    }    .dataframe thead th {        text-align: right;    }</style><table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>Time</th>      <th>TimePos</th>      <th>TimeNeg</th>      <th>UpperLimit</th>      <th>RatePos</th>      <th>RateNeg</th>      <th>FracExp</th>      <th>BGrate</th>      <th>BGerr</th>      <th>CorrFact</th>      <th>CtsInSrc</th>      <th>BGInSrc</th>      <th>Exposure</th>      <th>Sigma</th>      <th>SNR</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>246742.809</td>      <td>172770.106</td>      <td>-96881.981</td>      <td>0.001821</td>      <td>0.0</td>      <td>0.0</td>      <td>0.0364</td>      <td>0.000125</td>      <td>0.000005</td>      <td>1.6836</td>      <td>3.0</td>      <td>1.2247</td>      <td>9811.0649</td>      <td>1.4103</td>      <td>inf</td>    </tr>  </tbody></table></div>
<p>The individual hard/soft band data are simpler and have symmetric errors on the rate:</p>
<div style="width: 95%; max-height: 200px; overflow: scroll;"><style scoped>    .dataframe tbody tr th:only-of-type {        vertical-align: middle;    }    .dataframe tbody tr th {        vertical-align: top;    }    .dataframe thead th {        text-align: right;    }</style><table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>Time</th>      <th>TimePos</th>      <th>TimeNeg</th>      <th>Rate</th>      <th>RateErr</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>243.520</td>      <td>19.831</td>      <td>-22.794</td>      <td>1.323371</td>      <td>0.271083</td>    </tr>    <tr>      <th>1</th>      <td>292.350</td>      <td>31.176</td>      <td>-29.000</td>      <td>0.772638</td>      <td>0.174978</td>    </tr>    <tr>      <th>2</th>      <td>344.898</td>      <td>21.252</td>      <td>-21.372</td>      <td>1.128383</td>      <td>0.252669</td>    </tr>    <tr>      <th>3</th>      <td>396.489</td>      <td>32.344</td>      <td>-30.339</td>      <td>0.752788</td>      <td>0.168329</td>    </tr>    <tr>      <th>4</th>      <td>472.663</td>      <td>56.463</td>      <td>-43.830</td>      <td>0.469917</td>      <td>0.105224</td>    </tr>    <tr>      <th>5</th>      <td>594.830</td>      <td>69.690</td>      <td>-65.705</td>      <td>0.347482</td>      <td>0.078028</td>    </tr>    <tr>      <th>6</th>      <td>704.853</td>      <td>57.453</td>      <td>-40.332</td>      <td>0.478983</td>      <td>0.107709</td>    </tr>    <tr>      <th>7</th>      <td>823.036</td>      <td>74.665</td>      <td>-60.730</td>      <td>0.356802</td>      <td>0.078279</td>    </tr>    <tr>      <th>8</th>      <td>981.211</td>      <td>97.016</td>      <td>-83.510</td>      <td>0.260160</td>      <td>0.058751</td>    </tr>    <tr>      <th>9</th>      <td>1169.651</td>      <td>66.536</td>      <td>-91.425</td>      <td>0.294099</td>      <td>0.066134</td>    </tr>    <tr>      <th>10</th>      <td>1323.066</td>      <td>81.111</td>      <td>-86.879</td>      <td>0.305241</td>      <td>0.065412</td>    </tr>    <tr>      <th>11</th>      <td>1511.165</td>      <td>146.250</td>      <td>-106.988</td>      <td>0.183356</td>      <td>0.041583</td>    </tr>    <tr>      <th>12</th>      <td>1762.130</td>      <td>148.523</td>      <td>-104.715</td>      <td>0.193502</td>      <td>0.040547</td>    </tr>    <tr>      <th>13</th>      <td>6366.778</td>      <td>235.123</td>      <td>-253.803</td>      <td>0.075101</td>      <td>0.016944</td>    </tr>    <tr>      <th>14</th>      <td>7199.183</td>      <td>603.718</td>      <td>-597.281</td>      <td>0.045383</td>      <td>0.008396</td>    </tr>  </tbody></table></div>
<p>And the hardness ratios are likewise simple:</p>
<div style="width: 95%; max-height: 200px; overflow: scroll;"><style scoped>    .dataframe tbody tr th:only-of-type {        vertical-align: middle;    }    .dataframe tbody tr th {        vertical-align: top;    }    .dataframe thead th {        text-align: right;    }</style><table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>Time</th>      <th>TimePos</th>      <th>TimeNeg</th>      <th>HR</th>      <th>HRErr</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>243.520</td>      <td>19.831</td>      <td>-22.794</td>      <td>1.149509</td>      <td>0.344784</td>    </tr>    <tr>      <th>1</th>      <td>292.350</td>      <td>31.176</td>      <td>-29.000</td>      <td>0.566709</td>      <td>0.160379</td>    </tr>    <tr>      <th>2</th>      <td>344.898</td>      <td>21.252</td>      <td>-21.372</td>      <td>0.801010</td>      <td>0.240731</td>    </tr>    <tr>      <th>3</th>      <td>396.489</td>      <td>32.344</td>      <td>-30.339</td>      <td>0.775909</td>      <td>0.231541</td>    </tr>    <tr>      <th>4</th>      <td>472.663</td>      <td>56.463</td>      <td>-43.830</td>      <td>0.680760</td>      <td>0.197203</td>    </tr>    <tr>      <th>5</th>      <td>594.830</td>      <td>69.690</td>      <td>-65.705</td>      <td>0.562516</td>      <td>0.157879</td>    </tr>    <tr>      <th>6</th>      <td>704.853</td>      <td>57.453</td>      <td>-40.332</td>      <td>0.697443</td>      <td>0.203879</td>    </tr>    <tr>      <th>7</th>      <td>823.036</td>      <td>74.665</td>      <td>-60.730</td>      <td>0.809213</td>      <td>0.239284</td>    </tr>    <tr>      <th>8</th>      <td>981.211</td>      <td>97.016</td>      <td>-83.510</td>      <td>0.737809</td>      <td>0.219589</td>    </tr>    <tr>      <th>9</th>      <td>1169.651</td>      <td>66.536</td>      <td>-91.425</td>      <td>0.681327</td>      <td>0.199567</td>    </tr>    <tr>      <th>10</th>      <td>1323.066</td>      <td>81.111</td>      <td>-86.879</td>      <td>1.048259</td>      <td>0.322824</td>    </tr>    <tr>      <th>11</th>      <td>1511.165</td>      <td>146.250</td>      <td>-106.988</td>      <td>0.838212</td>      <td>0.258235</td>    </tr>    <tr>      <th>12</th>      <td>1762.130</td>      <td>148.523</td>      <td>-104.715</td>      <td>0.925555</td>      <td>0.267684</td>    </tr>    <tr>      <th>13</th>      <td>6366.778</td>      <td>235.123</td>      <td>-253.803</td>      <td>0.942488</td>      <td>0.298569</td>    </tr>    <tr>      <th>14</th>      <td>7199.183</td>      <td>603.718</td>      <td>-597.281</td>      <td>0.688193</td>      <td>0.165654</td>    </tr>  </tbody></table></div>
<hr class='heavy'/>
<h2 id="the-spectrum-dict">The Spectrum dict</h2>
<p>The spectrum <code>dict</code> contains, at core, information about extracted spectra and (if applicable) the fitted model(s).
An extra complexity arises because a given object will often have multiple spectra. To accommodate this the spectral
<code>dict</code> has, in all cases, three layers:</p>
<ol>
<li>The spectra that exist (i.e. the time intervals over which spectra were built)</li>
<li>The XRT Modes</li>
<li>The fitted spectral model(s)</li>
</ol>
<p>Even in cases where there is only one entry at a given level (e.g. there are only PC-mode data) all layers exist.
There are various relevant keywords in each layer as well. So, the conceptual map of a spectrum <code>dict</code> is as follows:</p>
<ul>
<li>'T0' - The reference time.</li>
<li>'DeltaFitStat' - The delta fit-statistic used in getting parameter errors.</li>
<li>'GalNH_unfitted' (optional): The Galactic absorption column towards the source.</li>
<li><strong>'rnames'</strong> - a list of all the time intervals for which spectra were built.</li>
<li>A <code>dict</code> for each entry in 'rname' which contains:
<ul>
<li>'DataFile' - A URL to get the data for this spectrum</li>
<li>'Start' - The start time of the requested time interval.</li>
<li>'Stop' - The end time of the requested time interval.</li>
<li><strong>'Modes'</strong> - a list of which XRT modes spectra were created</li>
<li>A <code>dict</code> for each entry in 'Modes' which contains:
<ul>
<li>'MeanTime' - The mean time of the events in the spectrum.</li>
<li>'Exposure' - The exposure time in the spectrum</li>
<li><strong>'Models'</strong> - A list of which models were fitted.</li>
<li>A <code>dict</code> for each entry in models, giving details of the spectral fit.</li>
</ul></li>
</ul></li>
</ul>
<p>Entries in boldface are lists, which give all the keys in the next layer.</p>
<p>Reading this in the abstract makes it looks rather more complex than it really is, and although I'll give an example
in a second, that en bloc is not really as readable as could be. So, perhaps the best way to explain
the concept is to show how you would actually access the spectral <code>dict</code>.</p>
<p>For <a href="https://www.swift.ac.uk/xrt_spectra">GRBs</a>,
there are normally two time slices, which (somewhat unhelpfully) are called &quot;interval0&quot; and &quot;late_time&quot;, and only a power-law model fit. If I have the spectrum <code>dict</code> for some GRB in the variable <code>mySpec</code>, and
I want to know what the best-fitting spectral index was for a power-law fit to the WT model &quot;interval0&quot; spectrum, I can just do:</p>
<pre><code class="language-python">print(mySpec['interval0']['WT']['Powerlaw']['Gamma])</code></pre>
<p>This is somewhat more readable (I hope). There are a lot of layers but the layout is clear and, as you may have noticed, the order
of the keys is just the inverse of the order of my prosaic statement, which, to me at least, seems logical. Of course, if you want something
beyond a spectral fit parameter then you need to check at what level it is relevant, but hopefully this is also logical (and you can check
it on the list above). For example, the exposure by the &quot;late_time&quot; PC mode spectrum doesn't depend on which model was
fitted, so this value appears at the &quot;rname/mode&quot; level.</p>
<p>So, to unpack this a bit more, I will give below a real spectrum <code>dict</code> for a GRB, and then I'll move on to the detailed expanation of each key.</p>
<p><strong>One important note first</strong>: In some cases it may be that the automated spectral fit failed, or you disabled
fitting; sometimes the spectrum for a given time interval could not be produced at all. In these cases the contents
of the various layers differ, as discussed <a href="#when-data-are-missing">further down this page</a>.</p>
<p>Right, let's take a look at a real spectrum <code>dict</code>. This is GRB 130925A, if you're interested, and I've added some
blank lines and indentation to try to make it a bit more readable.</p>
<pre><code class="language-python">{ 'T0': 401775096,
  'DeltaFitStat': 2.706,
  'rnames': ['interval0', 'late_time'],
  'interval0':{
    'DataFile': 'https://www.swift.ac.uk/xrt_spectra/00571830/interval0.tar.gz',
    'Start': 151.206299126148,
    'Stop': 40413.0104033947,
    'Modes': ['WT', 'PC'],
    'WT': {
      'Models': ['PowerLaw'],
      'PowerLaw': {
        'GalacticNH': 1.74728e+20,
        'NH': 2.61822e+22,
        'NHPos': 4.195329499999989e+20,
        'NHNeg': -4.114560899999997e+20,
        'Redshift_abs': 0.347,
        'Gamma': 1.74059,
        'GammaPos': 0.01495348799999996,
        'GammaNeg': -0.014803381000000115,
        'ObsFlux': 3.2308738407058433e-09,
        'ObsFluxPos': 2.0927980842864315e-11,
        'ObsFluxNeg': -2.0775434446476415e-11,
        'UnabsFlux': 5.272662824293303e-09,
        'UnabsFluxPos': 4.9185968693846606e-11,
        'UnabsFluxNeg': -4.730966359732954e-11,
        'Cstat': 1389.742568,
        'Dof': 960,
        'FitChi': 1347.730724,
        'Image': 'https://www.swift.ac.uk/xrt_spectra/00571830/interval0wt_plot.gif'
        },
      'Exposure': 3162.851695179939,
      'MeanTime': 3449.54543888569
      },

    'PC': {
      'Models': ['PowerLaw'],
      'PowerLaw': {
        'GalacticNH': 1.74728e+20,
        'NH': 3.05251e+22,
        'NHPos': 3.1388244100000005e+21,
        'NHNeg': -2.9426779299999997e+21,
        'Redshift_abs': 0.347,
        'Gamma': 2.59379,
        'GammaPos': 0.1405418380000003,
        'GammaNeg': -0.13220066099999972,
        'ObsFlux': 7.526620170564824e-11,
        'ObsFluxPos': 3.860703494878197e-12,
        'ObsFluxNeg': -3.6410524464384235e-12,
        'UnabsFlux': 2.772043237577702e-10,
        'UnabsFluxPos': 5.272611683802778e-11,
        'UnabsFluxNeg': -3.991673128151661e-11,
        'Cstat': 487.9061045,
        'Dof': 490,
        'FitChi': 496.7632034,
        'Image': 'https://www.swift.ac.uk/xrt_spectra/00571830/interval0pc_plot.gif'
        },
      'Exposure': 5029.643800079823,
      'MeanTime': 17427.6717456579
      }
  },

  'late_time': {
    'DataFile': 'https://www.swift.ac.uk/xrt_spectra/00571830/late_time.tar.gz',
    'Start': 5502.69384342432,
    'Stop': 40413.0104033947,
    'Modes': ['PC'],
    'PC': {
      'Models': ['PowerLaw'],
      'PowerLaw': {
        'GalacticNH': 1.74728e+20,
        'NH': 3.15504e+22,
        'NHPos': 3.276992999999999e+21,
        'NHNeg': -3.0701709200000014e+21,
        'Redshift_abs': 0.347,
        'Gamma': 2.68868,
        'GammaPos': 0.14820270499999966,
        'GammaNeg': -0.13902135400000004,
        'ObsFlux': 6.826529950876817e-11,
        'ObsFluxPos': 3.594728145422862e-12,
        'ObsFluxNeg': -3.3616900080457612e-12,
        'UnabsFlux': 2.852200160603111e-10,
        'UnabsFluxPos': 6.096089137778289e-11,
        'UnabsFluxNeg': -4.542858750653171e-11,
        'Cstat': 450.7716251,
        'Dof': 470,
        'FitChi': 458.30322,
        'Image': 'https://www.swift.ac.uk/xrt_spectra/00571830/late_timepc_plot.gif'
        },
      'Exposure': 4966.961300075054,
      'MeanTime': 18497.190929234
      }
  }
}</code></pre>
<p>Yowsers that's a lot to take in, but hopefully you can follow the structure. First, we had some information common
to all the spectra: the reference time and delta fitstat (discussed in a moment). Then the &quot;rnames&quot; list told us
that we have two spectra, &quot;interval0&quot; and &quot;late_time&quot;. If you follow the indentation levels you will see that
the remaining two keys in this top-level <code>dict</code> were indeed &quot;interval0&quot; and &quot;late_time&quot;. Within each of these
there was some information common to that spectral time-interval, and then &quot;Modes&quot;, telling us for which modes
spectra were produced in this time interval. Then we have the keys &quot;WT&quot; and &quot;PC&quot; in the &quot;interval0&quot; spectrum, or just
&quot;PC&quot; for the &quot;late_time&quot; spectrum, and so on through the structure.</p>
<p>Honestly, that's probably (more than) enough to be going on with. You may want to glance at <a href="#when-data-are-missing">When data are missing</a>,
for completeness, but unless you're having trouble sleeping, you should only read on when you want more detail about a specific entry.
If you are having trouble sleeping, make sure you use a blue-light filter on the device you're reading with.</p>
<p>OK, let's go through the actual keys one at a time. Yay.</p>
<p>First, the top-level <code>dict</code>.</p>
<h3 id="t0">T0</h3>
<p>'T0' is a reference time for the spectrum in Swift Mission Elapsed Time. All other times are given relative
to this. Please do read <a href="#metwarn">the notes on MET, above</a>.</p>
<h3 id="deltafitstat">DeltaFitStat</h3>
<p>'DeltaFitStat' relates to the errors on the fitted parameters. These are determined by <code>xspec</code> by
stepping the parameter of interest and refitting until the fit statistic has increased 'DeltaFitStat'.
Ordinarily this is either 1 (or 1-&sigma; errors) or 2.706 (for 90% confidence errors), but in some  cases
you can set this to whatever you want.</p>
<h3 id="galnh_unfitted">GalNH_unfitted</h3>
<p>The 'GalNH_unfitted' value only appears for spectra where a Galactic absorber was not used. In these cases the expected
Galactic column along the line of sight to the source is given in the top level of the spectrum <code>dict</code>. It is given
purely for information - it was not used at all - and was taken from <a href="https://ui.adsabs.harvard.edu/abs/2013MNRAS.431..394W/abstract">Willingale et al.,
(2013)</a>.</p>
<h3 id="rnames">rnames</h3>
<p>'rnames' is a list giving the labels applied to each time interval for which spectra were built. This essentially serves
as an index for the results. (NB 'rname' comes from 'region name', where a 'region' is a time region requested. Had I realised,
when writing the spectral code in 2008, that one day I was going to expose its workings via an API, I would have used
a better label).</p>
<p>That is it for the standard contents of the top level. There will still be one key for each entry in 'rnames',
containing the details of what was produced for that time interval. So, let's go through the contents of each of these now.</p>
<h3 id="datafile">DataFile</h3>
<p>The 'DataFile' entry contains a URL pointing to a '.tar.gz' archive which contains all of the files for the
spectra for this time interval. This can be used by you to download the spectrum if you want to fit or manipulate it
yourself. It is also used by the <a href="commonFunc.md#savespectra">saveSpectra()</a> function that appears throughout
the <code>swifttools.ukssdc</code> module.</p>
<h3 id="start">Start</h3>
<p>The 'Start' entry contains the start time in seconds since 'T0' of the <em>requested</em> time interval. This does not necessarily
correspond to the time covered by any of the actual spectra, since that depends on the availability of data.</p>
<h3 id="stop">Stop</h3>
<p>The 'Stop' entry contains the stop time in seconds since 'T0' of the <em>requested</em> time interval. This does not necessarily
correspond to the time covered by any of the actual spectra, since that depends on the availability of data.</p>
<h3 id="nospec">NOSPEC</h3>
<p>If no spectra could actually be created for this time interval, then the key 'NOSPEC' will exist, and the <code>dict</code> for this
time interval will terminate here.</p>
<h3 id="modes">Modes</h3>
<p>The 'Modes' key contains a list of the XRT modes for which spectra were created for this time interval.</p>
<p>And this is again, the end of the layer, the above defines the standard contents for each time interval.
But of course, there is now an entry for each of the modes (listed in 'Modes') for which we have a spectrum.
So, let's move on...</p>
<p>For each mode within each time interval, the <code>dict</code> will have these keys:</p>
<h3 id="meantime">MeanTime</h3>
<p>The 'MeanTime' entry contains the mean time of the X-ray events in the spectrum for this time interval and mode.
It is in seconds since T0.</p>
<h3 id="exposure">Exposure</h3>
<p>The 'Exposure' entry gives the exposure time, in seconds, in the spectrum for this time interval and mode.</p>
<h3 id="nofit">NOFIT</h3>
<p>If, when requesting spectra be built, you also requested that they not be fitted automatically then there will
be the 'NOFIT' key at this level and (strangely enough) no further information, since all that remains pertains to the
automated fits.</p>
<h3 id="models">Models</h3>
<p>The 'Models' key contains a list of the spectral models that were requested for fitting.</p>
<p>And we are now, finally, almost at an end. The only thing that remains at this level (time interval -&gt; XRT Mode) is
one entry for each model that was requested for automatic fitting. These have keys given in the 'Models' entry just described,
and they are themselves <code>dict</code>s. The keys of these <code>dict</code>s depend upon the model, you can see from the example
earlier a typical example: for a blackbody or APEC fit &quot;Gamma&quot; will be replaced with &quot;kT&quot; and whether or not a redshift
accompanies the absorber depends on the request via which the spectrum was built.</p>
<p>Sometimes the automated spectral fit fails. In this case there will be a 'NOFIT' entry at this level.</p>
<p>There is also a key &quot;Image&quot; which gives the URL to an image of the spectrum and fitted model.</p>
<p>Phew. If you're stll awake, well done!</p>
<h3 id="when-data-are-missing">When data are missing</h3>
<p>One very last thing to note. Sometimes, things can be missing. Below I have listed what can happen,
and what the spectrum <code>dict</code> looks like in these cases.</p>
<dl>
<dt>No spectrum exists for the object requested.</dt>
<dd>The top level of the <code>dict</code> contains the key &quot;NoSpectrum&quot;. The other keys are absent.</dd>
<dt>The spectrum for a given time interval could not be produced.</dt>
<dd>The [rname] <code>dict</code> for the given time interval contains the key &quot;NOSPEC&quot;; the &quot;Modes&quot; key is absent.</dd>
<dt>Automatic fitting was not requested for the spectrum.</dt>
<dd>The [rname][mode] <code>dict</code> for each time interval and mode contains the key &quot;NOFIT&quot;; the &quot;Models&quot; key is absent.
You may wonder why this isn't just given at the top level: the reason is that an [rname][mode] tree
still exists and contains all of the information about the spectrum, so it seems logical to indicate
that there is no fit at this level, where you will be otherwise looking for the &quot;Models&quot; entry.</dd>
<dt>The automatic fit could not be produced.</dt>
<dd>The [rname][mode][model] <code>dict</code> for the specific time interval, model and model contains the key &quot;NOFIT&quot;; the results
of the fit are (obviously) absent.</dd>
</dl>
<hr class='heavy'/>
<h2 id="the-burst-analyser-dict">The Burst analyser dict</h2>
<p>The burst analyser <code>dict</code> is a nested <code>dict</code> with several layers, just like the structures above.
The overall structure is</p>
<ul>
<li>Instruments
<ul>
<li>BAT binning</li>
<li>Light curves</li>
</ul></li>
</ul>
<p>but things are slightly more complicated; the &quot;BAT binning&quot; layer is only present in one of the &quot;Instrument&quot; layers (the
BAT) and hardness ratio data move around a bit. The full schematic is below, and I have skipped some of the data
(especially all the actual light curves) and added some comments to make this more readable. For a walkthrough of the
contents, see the <a href="data/GRB.md#burst-analyser"><code>swifttools.ukssdc.data.GRB</code> page</a>). The main point to note is that
this structure basically holds a lot of <a href="#the-light-curve-dict">light curve <code>dict</code>s</a>, organised by Swift instrument,
(by binning for BAT only), and by energy band. For BAT and XRT there is also a hardness ratio time series (which includes
the photon index and ECF inferred from the hardness ratio).</p>
<pre><code class="language-python">{
  'Instruments': ['BAT', 'BAT_NoEvolution', 'XRT', 'UVOT'],
  'BAT': {
    'HRData': &lt;a DataFrame containing the hardness ratio&gt;,
    'Binning': [
      'SNR4',
      'SNR4_sinceT0',
      'SNR5',
      'SNR5_sinceT0',
      'SNR6',
      'SNR6_sinceT0',
      'SNR7',
      'SNR7_sinceT0',
      'TimeBins_4ms',
      'TimeBins_64ms',
      'TimeBins_1s',
      'TimeBins_10s'],
    'SNR4': {
      'Datasets': ['ObservedFlux', 'Density', 'XRTBand', 'BATBand'],
      'ObservedFlux': &lt;a DataFrame containing the light curve&gt;,
      'Density': &lt;a DataFrame containing the light curve&gt;,
      'XRTBand': &lt;a DataFrame containing the light curve&gt;,
      'BATBand':  &lt;a DataFrame containing the light curve&gt;
    }
    'SNR4_sinceT0': {
      'Datasets': ['ObservedFlux', 'Density', 'XRTBand', 'BATBand'],
      'ObservedFlux': &lt;a DataFrame containing the light curve&gt;,
      'Density': &lt;a DataFrame containing the light curve&gt;,
      'XRTBand': &lt;a DataFrame containing the light curve&gt;,
      'BATBand':  &lt;a DataFrame containing the light curve&gt;
    }
    ... more entries, as above, one for each entry in 'Binning'

  }, # End of ['BAT']
  'BAT_NoEvolution': {
    'ECFs': {
      'ObservedFlux': 0.00243424007095474,
      'Density': 0.00231776220799315,
      'XRTBand': 4.70354458026304e-08,
      'BATBand': 6.85253672780114e-07
    },
    'Binning': [
      'SNR4',
      'SNR4_sinceT0',
      'SNR5',
      'SNR5_sinceT0',
      'SNR6',
      'SNR6_sinceT0',
      'SNR7',
      'SNR7_sinceT0',
      'TimeBins_4ms',
      'TimeBins_64ms',
      'TimeBins_1s',
      'TimeBins_10s']
    'SNR4': {
      'Datasets': ['ObservedFlux', 'Density', 'XRTBand', 'BATBand'],
      'ObservedFlux': &lt;a DataFrame containing the light curve&gt;,
      'Density': &lt;a DataFrame containing the light curve&gt;,
      'XRTBand': &lt;a DataFrame containing the light curve&gt;,
      'BATBand':  &lt;a DataFrame containing the light curve&gt;
    }
    'SNR4_sinceT0': {
      'Datasets': ['ObservedFlux', 'Density', 'XRTBand', 'BATBand'],
      'ObservedFlux': &lt;a DataFrame containing the light curve&gt;,
      'Density': &lt;a DataFrame containing the light curve&gt;,
      'XRTBand': &lt;a DataFrame containing the light curve&gt;,
      'BATBand':  &lt;a DataFrame containing the light curve&gt;
    }
    ... more entries, as above, one for each entry in 'Binning'
  }, # End of ['BAT_NoEvolution']

  'XRT': {
    'HRData_PC': &lt;a DataFrame containing the hardness ratio&gt;      
    'Datasets': [
      'ObservedFlux_PC_incbad',
      'Density_PC_incbad',
      'XRTBand_PC_incbad',
      'BATBand_PC_incbad'
    ],
    'ObservedFlux_PC_incbad': &lt;a DataFrame containing the light curve&gt;,
    'Density_PC_incbad': &lt;a DataFrame containing the light curve&gt;,
    'XRTBand_PC_incbad': &lt;a DataFrame containing the light curve&gt;,
  }, , # End of ['XRT']
  'UVOT': {
    'Datasets': ['white', 'b', 'u', 'v', 'uvw1', 'uvw2', 'uvm2']
    'white':  &lt;a DataFrame containing the light curve&gt;, 
    'b': &lt;a DataFrame containing the light curve&gt;,
    'u': &lt;a DataFrame containing the light curve&gt;,
    'v': &lt;a DataFrame containing the light curve&gt;,
    'uvw1': &lt;a DataFrame containing the light curve&gt;,
    'uvw2': &lt;a DataFrame containing the light curve&gt;
  }
}</code></pre></div>
      <div id="footer">        <p>
          UK Swift Science Data Centre<br/>
          Last updated <span id='PageFootDate'>2024 May 24</span><br/>  
          Web page maintained by Vatsalya Maddi<br/>
          E-mail: <a href="mailto:swifthelp@le.ac.uk">swift help</a><br/>
          Please read our <a href='/GDPR.php'>privacy notice</a>.
        </p>

      </div>  </body></html>