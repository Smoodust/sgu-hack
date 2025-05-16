import {
  Image,
  ModalDivider,
  ModuleBody,
  ModuleChild,
  ModuleChildTitle,
  ModuleChildValue,
  ModuleContainer,
  ModuleHeader,
} from '../styled/Modal.style';
import { Modal, Slide } from '@mui/material';
import close from '../assets/close.svg';
import ModalStore from '../stores/Modal.store';
import { observer } from 'mobx-react-lite';
import { useEffect } from 'react';
import API from '../utils/API';
const ModalComponent = observer(() => {
  useEffect(() => {
    API.getModalData().then((res) => {
      ModalStore.setModuleData('warnings', res['warnings']);
      ModalStore.setModuleData('errors', res['errors']);
      ModalStore.setModuleData('mainError', res['mainError']);
      ModalStore.setModuleData('possibleReason', res['possibleReason']);
      ModalStore.setModuleData('possiblePatch', res['possiblePatch']);
    });
  }, []);
  return (
    <Modal
      style={{ backdropFilter: 'blur(5px)' }}
      closeAfterTransition
      slotProps={{
        backdrop: {
          timeout: 500,
        },
      }}
      open={ModalStore.getOpen()}
      onClose={() => {
        ModalStore.setOpen(!ModalStore.getOpen());
      }}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Slide
        direction="up"
        in={ModalStore.getOpen()}
        timeout={{ enter: 500, exit: 500 }}
      >
        <ModuleContainer>
          <ModuleHeader>
            <Image src={close} onClick={() => ModalStore.setOpen(false)} />
          </ModuleHeader>
          <ModuleBody>
            <ModuleChild>
              <ModuleChildTitle>Пакет</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().name}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>Категория</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().category}
              </ModuleChildValue>
            </ModuleChild>
            <ModalDivider />
            <ModuleChild>
              <ModuleChildTitle>Warnings</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().warnings}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>Errors</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().errors}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>mainError</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().mainError}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>possibleReason</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().possibleReason}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>possiblePatch</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().possiblePatch}
              </ModuleChildValue>
            </ModuleChild>
          </ModuleBody>
        </ModuleContainer>
      </Slide>
    </Modal>
  );
});

export default ModalComponent;
