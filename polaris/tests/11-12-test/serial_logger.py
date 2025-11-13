import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


def parse_log_file(filename):
    """
    Parse the serial log file and extract data into a DataFrame.

    Args:
        filename: Path to the log file

    Returns:
        DataFrame with parsed data
    """
    data_lines = []

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Skip header lines and parse data
    for line in lines:
        # Look for lines with timestamps in brackets
        if line.startswith('['):
            # Extract the data after the timestamp
            parts = line.split('] ')
            if len(parts) > 1:
                data = parts[1].strip()
                # Skip debug messages like "Left Firing", "Right Firing", error numbers
                if ',' in data and not data.startswith('ERROR'):
                    data_lines.append(data)

    # Create DataFrame
    # Expected columns based on your CircuitPython code:
    # Time,Angular Position,R Solenoid,L Solenoid,Angular Vel X,Angular Vel Y,Angular Vel Z,PID Error,P,D
    columns = ['Delta_Time', 'Angular_Position', 'R_Solenoid', 'L_Solenoid',
               'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'PID_Output', 'Error', 'Derivative']

    # Parse the data
    parsed_data = []
    for line in data_lines:
        try:
            values = [float(x.strip()) for x in line.split(',')]
            if len(values) == len(columns):
                parsed_data.append(values)
        except ValueError:
            continue  # Skip lines that can't be parsed

    df = pd.DataFrame(parsed_data, columns=columns)

    # Create cumulative time column
    df['Time'] = df['Delta_Time'].cumsum()

    return df


def plot_gnc_data(df, output_prefix='gnc_analysis'):
    """
    Create comprehensive plots for GNC system analysis.

    Args:
        df: DataFrame with parsed GNC data
        output_prefix: Prefix for output image files
    """

    # Set up the plot style
    plt.style.use('seaborn-v0_8-darkgrid')

    # Create a figure with multiple subplots (reduced height to fit on screen)
    fig, axes = plt.subplots(5, 1, figsize=(12, 10))
    fig.suptitle('GNC System Performance Analysis', fontsize=16, fontweight='bold')

    # Plot 1: Angular Position vs Time
    ax1 = axes[0]
    ax1.plot(df['Time'], df['Angular_Position'], 'b-', linewidth=1.5, label='Heading')
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Target (0°)')
    ax1.axhline(y=90, color='g', linestyle='--', alpha=0.5, label='Target (90°)')
    ax1.axhline(y=180, color='orange', linestyle='--', alpha=0.5, label='Target (180°)')
    ax1.axhline(y=270, color='purple', linestyle='--', alpha=0.5, label='Target (270°)')
    ax1.set_xlabel('Time (s)', fontweight='bold')
    ax1.set_ylabel('Angular Position (°)', fontweight='bold')
    ax1.set_title('Heading Control Performance')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Plot 2: Angular Velocity (Gyro Data)
    ax2 = axes[1]
    ax2.plot(df['Time'], df['Gyro_X'], 'r-', linewidth=1, alpha=0.7, label='Gyro X')
    ax2.plot(df['Time'], df['Gyro_Y'], 'g-', linewidth=1, alpha=0.7, label='Gyro Y')
    ax2.plot(df['Time'], df['Gyro_Z'], 'b-', linewidth=1, alpha=0.7, label='Gyro Z')
    ax2.set_xlabel('Time (s)', fontweight='bold')
    ax2.set_ylabel('Angular Velocity (rad/s)', fontweight='bold')
    ax2.set_title('Angular Velocity (IMU Gyroscope)')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    # Plot 3: PID Error and Output
    ax3 = axes[2]
    ax3_twin = ax3.twinx()

    line1 = ax3.plot(df['Time'], df['Error'], 'r-', linewidth=1.5, label='Error')
    ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax3.set_xlabel('Time (s)', fontweight='bold')
    ax3.set_ylabel('Error (°)', fontweight='bold', color='r')
    ax3.tick_params(axis='y', labelcolor='r')

    line2 = ax3_twin.plot(df['Time'], df['PID_Output'], 'b-', linewidth=1.5, alpha=0.7, label='PID Output')
    ax3_twin.set_ylabel('PID Output', fontweight='bold', color='b')
    ax3_twin.tick_params(axis='y', labelcolor='b')

    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax3.legend(lines, labels, loc='upper right')
    ax3.set_title('PID Controller Performance')
    ax3.grid(True, alpha=0.3)

    # Plot 4: Thruster Activity
    ax4 = axes[3]

    # Create thruster activity visualization
    ax4.fill_between(df['Time'], 0, df['R_Solenoid'],
                     where=(df['R_Solenoid'] > 0),
                     color='yellow', alpha=0.6, label='Right Thruster (Negative Torque)')
    ax4.fill_between(df['Time'], 0, -df['L_Solenoid'],
                     where=(df['L_Solenoid'] > 0),
                     color='red', alpha=0.6, label='Left Thruster (Positive Torque)')

    ax4.set_xlabel('Time (s)', fontweight='bold')
    ax4.set_ylabel('Thruster State', fontweight='bold')
    ax4.set_title('Thruster Firing Activity')
    ax4.set_ylim([-1.5, 1.5])
    ax4.set_yticks([-1, 0, 1])
    ax4.set_yticklabels(['Left', 'Off', 'Right'])
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)

    # Plot 5: Error vs PID Output (Phase Plot)
    ax5 = axes[4]
    scatter = ax5.scatter(df['Error'], df['PID_Output'],
                          c=df['Time'], cmap='viridis',
                          alpha=0.6, s=10)
    ax5.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax5.axvline(x=0, color='k', linestyle='--', alpha=0.3)
    ax5.set_xlabel('Error (°)', fontweight='bold')
    ax5.set_ylabel('PID Output', fontweight='bold')
    ax5.set_title('PID Response Characteristic (Color = Time)')
    ax5.grid(True, alpha=0.3)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax5)
    cbar.set_label('Time (s)', rotation=270, labelpad=15)

    plt.tight_layout()

    # Save the figure
    output_file = f'{output_prefix}_full.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved comprehensive plot: {output_file}")

    # Create a second figure for duty cycle analysis
    fig2, (ax_duty, ax_freq) = plt.subplots(2, 1, figsize=(12, 6))
    fig2.suptitle('Thruster Usage Analysis', fontsize=16, fontweight='bold')

    # Duty Cycle Over Time (Rolling Window)
    window_size = 50  # Adjust based on data density
    if len(df) > window_size:
        df['R_Duty'] = df['R_Solenoid'].rolling(window=window_size).mean() * 100
        df['L_Duty'] = df['L_Solenoid'].rolling(window=window_size).mean() * 100

        ax_duty.plot(df['Time'], df['R_Duty'], 'y-', linewidth=2, label='Right Thruster Duty Cycle')
        ax_duty.plot(df['Time'], df['L_Duty'], 'r-', linewidth=2, label='Left Thruster Duty Cycle')
        ax_duty.set_xlabel('Time (s)', fontweight='bold')
        ax_duty.set_ylabel('Duty Cycle (%)', fontweight='bold')
        ax_duty.set_title(f'Thruster Duty Cycle (Rolling Average, Window={window_size})')
        ax_duty.legend(loc='upper right')
        ax_duty.grid(True, alpha=0.3)

    # Overall Statistics
    total_time = df['Time'].iloc[-1] - df['Time'].iloc[0]
    r_on_time = df['R_Solenoid'].sum() * df['Delta_Time'].mean()
    l_on_time = df['L_Solenoid'].sum() * df['Delta_Time'].mean()

    r_duty = (r_on_time / total_time) * 100 if total_time > 0 else 0
    l_duty = (l_on_time / total_time) * 100 if total_time > 0 else 0

    ax_freq.bar(['Right Thruster', 'Left Thruster'], [r_duty, l_duty],
                color=['yellow', 'red'], alpha=0.7, edgecolor='black')
    ax_freq.set_ylabel('Overall Duty Cycle (%)', fontweight='bold')
    ax_freq.set_title('Overall Thruster Usage')
    ax_freq.grid(True, alpha=0.3, axis='y')

    # Add text annotations
    ax_freq.text(0, r_duty + 1, f'{r_duty:.1f}%', ha='center', fontweight='bold')
    ax_freq.text(1, l_duty + 1, f'{l_duty:.1f}%', ha='center', fontweight='bold')

    plt.tight_layout()

    output_file2 = f'{output_prefix}_duty.png'
    plt.savefig(output_file2, dpi=300, bbox_inches='tight')
    print(f"Saved duty cycle analysis: {output_file2}")

    # Create a third figure for Time vs Velocity (like your image)
    fig3, ax_vel = plt.subplots(1, 1, figsize=(12, 6))

    # Calculate total angular velocity magnitude (Z-axis is primary rotation)
    # Use Gyro_Z as the main angular velocity
    angular_velocity = df['Gyro_Z']

    # Plot with thruster states overlaid
    scatter = ax_vel.scatter(df['Time'], angular_velocity,
                             c=['yellow' if r else ('red' if l else 'blue')
                                for r, l in zip(df['R_Solenoid'], df['L_Solenoid'])],
                             s=20, alpha=0.8, edgecolors='none')

    ax_vel.axhline(y=0, color='k', linestyle='-', alpha=0.3, linewidth=1)
    ax_vel.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
    ax_vel.set_ylabel('Angular Velocity (Rotations per Second)', fontweight='bold', fontsize=12)
    ax_vel.set_title('Time vs Velocity', fontsize=14, fontweight='bold')
    ax_vel.grid(True, alpha=0.3)

    # Create custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='blue', label='No Thruster'),
        Patch(facecolor='yellow', label='Right Thruster'),
        Patch(facecolor='red', label='Left Thruster')
    ]
    ax_vel.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()

    output_file3 = f'{output_prefix}_velocity.png'
    plt.savefig(output_file3, dpi=300, bbox_inches='tight')
    print(f"Saved velocity plot: {output_file3}")

    # Create a fourth figure for Heading vs Time
    fig4, ax_heading = plt.subplots(1, 1, figsize=(12, 6))

    # Plot heading with thruster states overlaid
    scatter = ax_heading.scatter(df['Time'], df['Angular_Position'],
                                 c=['yellow' if r else ('red' if l else 'blue')
                                    for r, l in zip(df['R_Solenoid'], df['L_Solenoid'])],
                                 s=20, alpha=0.8, edgecolors='none')

    # Add target heading line
    ax_heading.axhline(y=0, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Target (0°)')

    # Overlay thruster activity on secondary y-axis
    ax_heading_twin = ax_heading.twinx()

    # Create thruster signal (+1 for right, -1 for left, 0 for off)
    thruster_signal = df['R_Solenoid'].astype(int) - df['L_Solenoid'].astype(int)

    ax_heading_twin.fill_between(df['Time'], 0, thruster_signal,
                                 where=(thruster_signal > 0),
                                 color='yellow', alpha=0.3, label='Right Thruster', step='post')
    ax_heading_twin.fill_between(df['Time'], 0, thruster_signal,
                                 where=(thruster_signal < 0),
                                 color='red', alpha=0.3, label='Left Thruster', step='post')

    ax_heading_twin.set_ylabel('Thruster Output', fontweight='bold', fontsize=12)
    ax_heading_twin.set_ylim([-1.5, 1.5])
    ax_heading_twin.set_yticks([-1, 0, 1])
    ax_heading_twin.set_yticklabels(['Left', 'Off', 'Right'])

    ax_heading.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
    ax_heading.set_ylabel('Heading (Degrees)', fontweight='bold', fontsize=12)
    ax_heading.set_title('Time vs Heading with Thruster Activity', fontsize=14, fontweight='bold')
    ax_heading.grid(True, alpha=0.3)

    # Combine legends from both axes
    lines1, labels1 = ax_heading.get_legend_handles_labels()
    lines2, labels2 = ax_heading_twin.get_legend_handles_labels()
    ax_heading.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    plt.tight_layout()

    output_file4 = f'{output_prefix}_heading.png'
    plt.savefig(output_file4, dpi=300, bbox_inches='tight')
    print(f"Saved heading plot: {output_file4}")

    # Print summary statistics
    print("\n" + "=" * 60)
    print("GNC SYSTEM PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"Test Duration: {total_time:.2f} seconds")
    print(f"\nHeading Statistics:")
    print(f"  Mean Position: {df['Angular_Position'].mean():.2f}°")
    print(f"  Std Dev: {df['Angular_Position'].std():.2f}°")
    print(f"  Range: {df['Angular_Position'].min():.2f}° to {df['Angular_Position'].max():.2f}°")
    print(f"\nError Statistics:")
    print(f"  Mean Error: {df['Error'].mean():.2f}°")
    print(f"  RMS Error: {np.sqrt((df['Error'] ** 2).mean()):.2f}°")
    print(f"  Max Error: {df['Error'].abs().max():.2f}°")
    print(f"\nThruster Usage:")
    print(f"  Right Thruster Duty Cycle: {r_duty:.1f}%")
    print(f"  Left Thruster Duty Cycle: {l_duty:.1f}%")
    print(f"  Total Active Time: {(r_on_time + l_on_time):.2f}s")
    print("=" * 60 + "\n")

    plt.show()


if __name__ == "__main__":
    # List available files in serial_logs directory
    log_dir = "serial_logs"
    if os.path.exists(log_dir):
        files = [f for f in os.listdir(log_dir) if f.endswith('.csv')]
        if files:
            files.sort()
            print("\nAvailable log files:")
            print("-" * 40)
            for i, f in enumerate(files, 1):
                file_path = os.path.join(log_dir, f)
                size = os.path.getsize(file_path)
                print(f"{i}. {f} ({size / 1024:.1f} KB)")
            print("-" * 40)

    # Prompt user for filename
    filename = input("\nEnter the log file path (or just filename if in serial_logs/): ").strip()

    # If user just entered a filename without path, check serial_logs directory
    if not os.path.exists(filename) and os.path.exists(log_dir):
        potential_path = os.path.join(log_dir, filename)
        if os.path.exists(potential_path):
            filename = potential_path

    # Verify file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        sys.exit(1)

    print(f"Analyzing data from: {filename}")

    # Parse and plot
    df = parse_log_file(filename)

    if len(df) == 0:
        print("No valid data found in file!")
        sys.exit(1)

    print(f"Loaded {len(df)} data points")

    # Generate output filename based on input
    output_prefix = os.path.splitext(filename)[0]

    plot_gnc_data(df, output_prefix)