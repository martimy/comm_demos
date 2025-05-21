import heapq
import random

class StopAndWaitSimulator:
    def __init__(self, tp, tf, ta, num_frames, frame_error_prob=0.1):
        """
        Stop-and-Wait ARQ simulator with error simulation.

        Parameters:
        - tp: propagation delay (one way)
        - tf: frame transmission time
        - ta: processing time at receiver
        - num_frames: total frames to simulate
        - frame_error_prob: probability of frame being corrupted
        """
        self.tp = tp
        self.tf = tf
        self.ta = ta
        self.num_frames = num_frames
        self.frame_error_prob = frame_error_prob

        self.current_time = 0.0
        self.event_list = []
        self.sent_count = 0
        self.current_seq = 0  # Frame number to send next
        self.waiting_for_ack = 0  # Last successfully sent frame (expected ACK)

    def schedule_event(self, event_time, event_type, event_data=None):
        heapq.heappush(self.event_list, (event_time, event_type, event_data))

    def handle_send(self, frame):
        """Send a frame to the receiver."""
        print(f"Sending Frame {frame['seq']} at time {self.current_time:.4f}")

        # Simulate frame error
        corrupted = random.random() < self.frame_error_prob
        if corrupted:
            print(f"  Frame {frame['seq']} will be received in ERROR")

        # ACK arrives after tf + 2tp + ta
        ack_arrival_time = self.current_time + self.tf + 2 * self.tp + self.ta

        if corrupted:
            ack_seq = frame['seq']  # NACK (receiver expects same frame again)
        else:
            ack_seq = (frame['seq'] + 1) % 2  # Expected next frame

        self.schedule_event(ack_arrival_time, "ack", {"ack": ack_seq, "original_seq": frame["seq"], "corrupted": corrupted})

    def handle_ack(self, ack):
        """Process ACK received by sender."""
        print(f"Received ACK {ack['ack']} at time {self.current_time:.4f} (for Frame {ack['original_seq']})")

        if ack['ack'] != ((ack['original_seq'] + 1) % 2):
            # NACK or duplicate ACK — retransmit same frame
            print(f"  --> Retransmitting Frame {ack['original_seq']}")
            self.schedule_event(self.current_time, "send", {"seq": ack['original_seq']})
        else:
            # Successful ACK — move to next frame
            self.sent_count += 1
            if self.sent_count < self.num_frames:
                self.current_seq = ack['ack']
                self.schedule_event(self.current_time, "send", {"seq": self.current_seq})

    def run_simulation(self):
        self.schedule_event(0.0, "send", {"seq": self.current_seq})
        while self.event_list:
            event_time, event_type, event_data = heapq.heappop(self.event_list)
            self.current_time = event_time

            if event_type == "send":
                self.handle_send(event_data)
            elif event_type == "ack":
                self.handle_ack(event_data)


# Example usage
if __name__ == "__main__":
    # Parameters
    tp = 5.0      # Propagation delay
    tf = 1.0      # Frame transmission time
    ta = 0.5      # Processing time at receiver
    num_frames = 10
    frame_error_prob = 0.1  # 20% chance of frame corruption

    simulator = StopAndWaitSimulator(tp, tf, ta, num_frames, frame_error_prob)
    simulator.run_simulation()
