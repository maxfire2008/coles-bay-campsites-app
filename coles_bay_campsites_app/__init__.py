def load_git():
    import os
    if not os.path.exists('/repositories_initial_load'):
        with open('/repositories_initial_load', 'w') as f:
            f.write('')

        os.system(
            "find ../repositories -mindepth 1 -maxdepth 1 -type d " +
            "-exec git -C {} pull \; 2>&1 > /dev/null"
        )
    else:
        print("Repositories already loading")

load_git()
