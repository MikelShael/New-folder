import streamlit as st
import itertools
import streamlit.components.v1 as components

# Function to generate combinations
def generate_combinations(indicator_name, case, input_definitions):
    input_values = []
    for input_def in input_definitions:
        if input_def['constant']:
            constant_value = input_def['value']
            input_values.append([constant_value])
        else:
            if input_def['type'] == 'Integer':
                start = int(input_def['start'])
                end = int(input_def['end'])
                step = int(input_def['step'])
                input_values.append(list(range(start, end + 1, step)))
            else:
                start = float(input_def['start'])
                end = float(input_def['end'])
                step = float(input_def['step'])
                input_values.append([round(i, 5) for i in list(drange(start, end, step))])

    # Generate all combinations (Cartesian product)
    combinations = list(itertools.product(*input_values))
    return combinations

# Custom range function for float step size
def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

# Function to apply conditions to the combinations
def apply_conditions(combinations, condition):
    valid_combinations = []
    for combo in combinations:
        input1_idx = condition['input1'] - 1  # Adjust for 0-based index
        input2_idx = condition['input2'] - 1
        diff = condition['min_difference']
        
        # Apply conditions
        if condition['relation'] == 'none':
            valid_combinations.append(combo)
        elif condition['relation'] == 'greater than':
            if combo[input1_idx] > combo[input2_idx] + diff:
                valid_combinations.append(combo)
        elif condition['relation'] == 'less than':
            if combo[input1_idx] < combo[input2_idx] and (combo[input2_idx] - combo[input1_idx]) >= diff:
                valid_combinations.append(combo)
    return valid_combinations

# Function to format float values by replacing '.' with '__'
def format_value(value):
    if isinstance(value, float):
        return str(value).replace('.', '__')
    return str(value)

# Streamlit App
st.title("Indicator Combination Generator with Conditions")

# Step 1: Enter indicator name and case
indicator_name = st.text_input("Enter the short name of the indicator:")
case = st.text_input("Enter the case (e.g., 'A'):")

# Step 2: Select the number of inputs
num_inputs = st.slider("Enter the number of inputs", min_value=1, max_value=10, value=3)

# Step 3: Dynamically create fields for each input
input_definitions = []
for i in range(num_inputs):
    st.subheader(f"Input {i+1}")
    
    constant = st.checkbox(f"Is Input {i+1} constant?", key=f"constant_{i}")

    input_type = st.radio(f"Choose the type for Input {i+1}", ('Integer', 'Float'), key=f"type_{i}")

    if constant:
        # Allow input as float or integer based on the type
        if input_type == 'Integer':
            value = st.number_input(f"Enter the constant value for Input {i+1} (integer)", key=f"value_{i}", step=1, format="%d")
        else:
            value = st.number_input(f"Enter the constant value for Input {i+1} (float)", key=f"value_{i}", step=0.01, format="%.5f")
        input_definitions.append({'constant': True, 'value': value, 'type': input_type})
    else:
        # Input for start, end, and step based on type
        if input_type == 'Integer':
            start = st.number_input(f"Enter the starting value for Input {i+1} (integer)", key=f"start_{i}", step=1, format="%d")
            end = st.number_input(f"Enter the ending value for Input {i+1} (integer)", key=f"end_{i}", step=1, format="%d")
            step = st.number_input(f"Enter the step size for Input {i+1} (integer)", key=f"step_{i}", min_value=1, value=1, step=1, format="%d")
        else:
            start = st.number_input(f"Enter the starting value for Input {i+1} (float)", key=f"start_{i}", step=0.01, format="%.5f")
            end = st.number_input(f"Enter the ending value for Input {i+1} (float)", key=f"end_{i}", step=0.01, format="%.5f")
            step = st.number_input(f"Enter the step size for Input {i+1} (float)", key=f"step_{i}", min_value=0.01, value=0.01, step=0.01, format="%.5f")
        
        input_definitions.append({'constant': False, 'start': start, 'end': end, 'step': step, 'type': input_type})

# Step 4: Define condition between inputs (aligned left to right)
st.subheader("Define Condition Between Inputs")

col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    input1 = st.selectbox("Choose Input", range(1, num_inputs + 1), key="cond_input1")
with col2:
    relation = st.selectbox("Condition", ["none", "greater than", "less than"], key="cond_relation", index=0)  # Default: no condition
with col3:
    input2 = st.selectbox("Choose Input", range(1, num_inputs + 1), key="cond_input2")

# Add an optional field for the minimum difference (only if a condition is selected)
if relation != 'none':
    min_difference = st.number_input("Min. Difference (optional)", min_value=0, value=0, key="cond_diff")
else:
    min_difference = 0  # If no condition, no difference

# Step 5: Generate and display combinations
if st.button("Generate Combinations"):
    if indicator_name and case and input_definitions:
        combinations = generate_combinations(indicator_name, case, input_definitions)
        
        # Apply the condition
        condition = {
            'input1': input1,
            'relation': relation,
            'input2': input2,
            'min_difference': min_difference
        }
        if relation != 'none':
            combinations = apply_conditions(combinations, condition)
        
        # Join combinations as a CSV and add a trailing comma at the end
        csv_combinations = ", ".join([f"{indicator_name}_{case}_" + "_".join(format_value(value) for value in combo) for combo in combinations]) + ','

        # Custom HTML for styled output with copy button
        components.html(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px; background-color: #2C2F33; border-radius: 10px; color: white; font-family: Arial, sans-serif;">
                <span>Combinations</span>
                <button onclick="navigator.clipboard.writeText(`{csv_combinations}`)" 
                style="background-color: #5865F2; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">Code kopieren</button>
            </div>
            <div style="margin-top: 10px; padding: 10px; background-color: #23272A; border-radius: 10px; color: white; font-family: monospace;">
                {csv_combinations}
            </div>
            """,
            height=200,
        )
    else:
        st.warning("Please fill all fields before generating combinations.")
