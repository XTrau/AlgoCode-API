def get_output_and_runtime(output):
    program_output, runtime, *_ = output.decode().split("\t")
    program_output = program_output.rstrip("\n\nreal")
    runtime = runtime.rstrip("\nuser")
    _, runtime = runtime.split("m")
    runtime = float(runtime)
    return program_output, runtime
