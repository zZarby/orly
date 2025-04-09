

-----  
### <p align="center">☁️ ORLY ☁️</p>

<br>
<p align="center">
<strong>
Yes, if you are looking for an open-source module to automatically import your dependencies and handle installation errors with ease, you are in the right place!
</strong>
</p>
<br>

-----  
### <p align="center">✔ Basic Example ✔</p>

```python
import orly
orly.set([
    'requests',
    'os'
])

print(requests.get('https://nohello.net').status_code)
```

-----  
### <p align="center">⚙️ Features ⚙️</p>

- ✅ Auto-installs missing modules using `pip`
- ✅ Supports aliasing (`module~~alias`)
- ✅ Handles modules with different pip names (`py_mod==pip_package`)
- ✅ Silent mode to suppress internal logs/prints (`*`)
- ✅ Compatible with Linux systems requiring `--break-system-packages`
- ✅ Clean console output (auto clear after each import)

-----  
### <p align="center">🧠 Advanced Usage 🧠</p>

```python
import orly
orly.set([
    'requests~~req',            # 'requests' accessible as 'req'
    'bs4==beautifulsoup4',      # 'bs4' is imported; pip package name is "beautifulsoup4"
    'discord',                  # Normal import
    'discord.ext.commands*'     # Silent import of submodule
])
```

> 🛑 Appending `*` to the module string makes it **silent**:  
> ‣ Disables `print()` from the module (if possible)  
> ‣ Disables logging propagation

You can also globally silence everything:

```python
orly.set(['requests', 'pandas', 'numpy'], silent=True)
```

-----  
### <p align="center">💖 Auto-Setup 💖</p>

```python
try: 
    import orly
except ImportError:
    try:
        __import__('subprocess').check_call([__import__('sys').executable, "-m", "pip", "install", "orly"])
    except:
        __import__('subprocess').check_call([__import__('sys').executable, "-m", "pip", "install", "orly", "--break-system-packages"])
    finally: 
        import orly
```

-----  
### <p align="center">📌 Disclaimer 📌</p>

<br>
- This project is for educational purposes only.
- Do not use this in any harmful, malicious or unethical way.
- I decline any responsibility for misuse.

-----  
### <p align="center">by Zarby</p>

