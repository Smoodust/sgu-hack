import torch
from torch import nn
from torch.nn import functional as F
from clearml import Task, OutputModel, Logger
from data_torch import get_train_dataloader, get_test_dataloader

log_interval = 50
device = torch.device("cpu")


def init_model() -> nn.Module:
    return nn.Linear(10, 10)


def init_optimizer(model: nn.Module):
    return torch.optim.Adam(model.parameters())


def loss_fn(output, target, reduction="avg"):
    if reduction == "avg":
        return F.nll_loss(output, target, reduction="mean")
    if reduction == "sum":
        return F.nll_loss(output, target, reduction="sum")
    return F.nll_loss(output, target)


def train_step(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    train_loader: torch.utils.data.DataLoader,
    device: torch.device,
    epoch: int,
) -> nn.Module:
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = loss_fn(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            Logger.current_logger().report_scalar(
                "train",
                "loss",
                iteration=(epoch * len(train_loader) + batch_idx),
                value=loss.item(),
            )
            print(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                    epoch,
                    batch_idx,
                    len(train_loader),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                )
            )
    return model


def test_step(
    model: nn.Module,
    test_loader: torch.utils.data.DataLoader,
    device: torch.device,
    epoch: int,
):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += loss_fn(
                output, target, reduction="sum"
            ).item()  # sum up batch loss
            pred = output.argmax(
                dim=1, keepdim=True
            )  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader)

    Logger.current_logger().report_scalar(
        "test", "loss", iteration=epoch, value=test_loss
    )
    Logger.current_logger().report_scalar(
        "test", "accuracy", iteration=epoch, value=(correct / len(test_loader))
    )
    print(
        "\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
            test_loss,
            correct,
            len(test_loader),
            100.0 * correct / len(test_loader),
        )
    )


def get_example_inputs() -> tuple[torch.Tensor]:
    return (torch.randn(1, 10),)


# Initialize ClearML Task
task = Task.init(project_name="Your Project", task_name="Nightly Training")

# Train your model
train_dataloader = get_train_dataloader()
test_dataloader = get_test_dataloader()

model = init_model()
optimizer = init_optimizer(model)

for epoch in range(5):
    model = train_step(model, optimizer, train_dataloader, device, epoch)
    test_step(model, test_dataloader, device, epoch)

example_inputs = get_example_inputs()
onnx_program = torch.onnx.export(model, example_inputs, dynamo=True)
if onnx_program is None:
    raise Exception()

# Save ONNX model
onnx_path = "model.onnx"
onnx_program.save(onnx_path)

# Upload to ClearML Model Registry
output_model = OutputModel(task=task)
output_model.update_weights(onnx_path)
output_model.publish()

task.close()
