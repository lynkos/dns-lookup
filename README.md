# DNS Lookup
> The goal of this project is to practice UDP socket programing and understand binary packet structures by developing a simplified DNS lookup client.
> You must create your own socket and cannot use any existing DNS library.

## Requirements
- [x] <a target="_blank" href="https://docs.continuum.io/free/anaconda/install">Anaconda</a> **OR** <a target="_blank" href="https://docs.conda.io/projects/miniconda/en/latest">Miniconda</a>

> [!TIP]
> If you have trouble deciding between Anaconda and Miniconda, please refer to the table below:
> <table>
>  <thead>
>   <tr>
>    <th><center>Anaconda</center></th>
>    <th><center>Miniconda</center></th>
>   </tr>
>  </thead>
>  <tbody>
>   <tr>
>    <td>New to conda and/or Python</td>
>    <td>Familiar with conda and/or Python</td>
>   </tr>
>   <tr>
>    <td>Not familiar with using terminal and prefer GUI</td>
>    <td>Comfortable using terminal</td>
>   </tr>
>   <tr>
>    <td>Like the convenience of having Python and 1,500+ scientific packages automatically installed at once</td>
>    <td>Want fast access to Python and the conda commands and plan to sort out the other programs later</td>
>   </tr>
>   <tr>
>    <td>Have the time and space (a few minutes and 3 GB)</td>
>    <td>Don't have the time or space to install 1,500+ packages</td>
>   </tr>
>   <tr>
>    <td>Don't want to individually install each package</td>
>    <td>Don't mind individually installing each package</td>
>   </tr>
>  </tbody>
> </table>
>
> Typing out entire Conda commands can sometimes be tedious, so I wrote a shell script ([`conda_shortcuts.sh` on GitHub Gist](https://gist.github.com/lynkos/7a4ce7f9e38bb56174360648461a3dc8)) to define shortcuts for commonly used Conda commands.
> <details>
>   <summary>Example: Delete/remove a conda environment named <code>test_env</code></summary>
>
> * Shortcut command
>     ```
>     rmenv test_env
>     ```
> * Manually typing out the entire command
>     ```sh
>     conda env remove -n test_env && rm -rf $(conda info --base)/envs/test_env
>     ```
>
> The shortcut has 80.8% fewer characters!
> </details>

## Installation
1. Verify that conda is installed
   ```
   conda --version
   ```

2. Ensure conda is up to date
   ```
   conda update conda
   ```

3. Enter the directory you want `dns-lookup` to be cloned in
   * POSIX
      ```sh
      cd ~/path/to/directory
      ```
   * Windows
      ```sh
      cd C:\Users\user\path\to\directory
      ```

4. Clone and enter `dns-lookup`
   ```sh
   git clone https://github.com/lynkos/dns-lookup.git && cd dns-lookup
   ```

5. Create virtual environment from [`environment.yml`](environment.yml)
   ```sh
   conda env create -f environment.yml
   ```

## Usage
<ol>
   <li>Activate <code>dns_env</code> (i.e., virtual environment)<pre>conda activate dns_env</pre></li>
   <li>Confirm <code>dns_env</code> is active
      <ul>
        <li><code>dns_env</code> should be in parentheses () or brackets [] before your command prompt, e.g.<pre>(dns_env) $</pre></li>
        <li>See which virtual environments are available and/or currently active (active environment denoted with asterisk (*))<pre>conda info --envs</pre> <b>OR</b> <pre>conda env list</pre></li>
      </ul>
   </li>
   <li>Run <a href="mydns.py"><code>mydns.py</code></a> (<code>domain-name</code> is the domain name to be resolved while <code>root-dns-ip</code> is the IPv4 address of a <a target="_blank" href="https://www.iana.org/domains/root/servers">root DNS server</a> on the internet)<pre>python mydns.py domain-name root-dns-ip</pre></li>
   <li>Deactivate <code>dns_env</code> (i.e., virtual environment) when finished<pre>conda deactivate</pre></li>
</ol>
